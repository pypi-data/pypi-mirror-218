import os
import shutil
import sys
import typing as tp
from pathlib import Path
from threading import Thread

from colorama import Fore
from colorama import Style
from redis import Redis

from webhooklib import config
from webhooklib import exceptions
from webhooklib.models import Resource
from webhooklib.models import ShellCommand
from webhooklib.models import ShellResult
from webhooklib.process_wrapper import run_subprocess

ENV_PREFIX = 'WEBHOOK_ENV_'


def red(obj: tp.Any) -> str:
    return f'{Fore.RED}{obj}{Style.RESET_ALL}'


def get_job_resources_names() -> frozenset[str]:
    res_string = os.environ.get('WEBHOOK_JOB_RESOURCES')
    if res_string is None:
        return frozenset()
    return frozenset(res_string.split(','))


def get_job_resources(all_resources) -> list[Resource]:
    return [
        all_resources[name]
        for name in get_job_resources_names()
    ]


def get_all_resources(resources_key: str, redis: Redis) -> dict[str, Resource]:
    pipeline = redis.pipeline()
    keys = redis.keys(f'{resources_key}:*')
    names = []
    for key in keys:
        pipeline.hgetall(key)
        _, name = key.rsplit(':', maxsplit=1)
        names.append(name)
    _resources = pipeline.execute()
    return {name: Resource(**r, key=k, name=name) for r, k, name in zip(_resources, keys, names, strict=True)}


def get_wait_resources(all_resources) -> dict[str, Resource]:
    job_resources = get_job_resources_names()
    return {
        name: resource
        for name, resource in all_resources.items()
        if name in set(job_resources) or name == 'job'
    }


def wait_message(channel: str, redis: Redis) -> None:
    p = redis.pubsub()
    p.subscribe(channel)
    while not (message := p.get_message(ignore_subscribe_messages=True)):
        pass
    print(message)


def wait_resource_semaphore(
    resource: Resource,
    job_stop_channel: str,
    redis: Redis,
) -> None:
    print('wait_resource_semaphore:', resource)
    try:
        pass
    except AttributeError:
        print('>>= AttributeError for resource: usage_current', resource)
        raise
    if resource.usage_current < resource.usage_limit:
        return
    print('resource busy, waiting... :', resource)
    wait_message(job_stop_channel, redis)
    wait_resources_semaphore(resource, job_stop_channel, redis)


def wait_resources_semaphore(
    resources: list[Resource],
    job_stop_channel: str,
    redis: Redis,
) -> None:
    for resource in resources:
        wait_resource_semaphore(resource, job_stop_channel, redis)


def lock_resources_semaphore(all_resources, redis: Redis):
    for resource in get_job_resources(all_resources):
        print('lock_resources_semaphore: increment +1', resource)
        redis.hincrby(resource.key, 'usage_current')


def unlock_resources_semaphore(all_resources, redis: Redis):
    for resource in get_job_resources(all_resources):
        print('unlock_resources_semaphore: decrement -1', resource)
        redis.hincrby(resource.key, 'usage_current', -1)


def read_rest_logs(redis: Redis, stdout_key: str, stderr_key: str) -> None:
    pipeline = redis.pipeline()
    pipeline.lrange(stdout_key, 1, -1)
    pipeline.lrange(stderr_key, 1, -1)
    stdout, stderr = pipeline.execute()
    for line in stdout:
        print(line, end='')
    for line in stderr:
        print(red(line), end='')


def main(line_buffer_size: int = 100):
    redis = Redis.from_url(os.environ['REDIS_URL'], decode_responses=True)

    all_resources = get_all_resources(os.environ['WEBHOOK_RESOURCES_KEY'], redis)
    wait_resources = get_wait_resources(all_resources)
    wait_resources_semaphore(list(wait_resources.values()), os.environ['WEBHOOK_JOB_STOP_CHANNEL'], redis)
    lock_resources_semaphore(all_resources, redis)

    # wait_max_jobs_quota(redis)
    # redis.incr(os.environ['WEBHOOK_N_JOBS_KEY'])
    redis.hincrby(all_resources['job'].key, 'usage_current')

    payload: dict[str, tp.Any] = {
        'cmd': sys.argv[1:],
    }
    if 'WEBHOOK_CWD' in os.environ:
        payload['cwd'] = os.environ['WEBHOOK_CWD']
    if 'WEBHOOK_TIMEOUT' in os.environ:
        payload['timeout'] = float(os.environ['WEBHOOK_TIMEOUT'])

    env = {
        k.removeprefix(ENV_PREFIX): v
        for k, v in os.environ.items()
        if k.startswith(ENV_PREFIX)
    }
    print(env)
    print(payload)
    command = ShellCommand(**payload)
    if shutil.which(command.cmd[0]) is None:
        raise exceptions.CmdNotFoundError(command.cmd[0])
    if command.cwd is not None:
        cwd = Path(command.cwd)
        if not (cwd.is_dir() and cwd.exists()):
            raise exceptions.CwdNotFoundError(command.cwd)

    t = Thread(target=run_subprocess, args=(command,))
    t.start()
    redis.set(f'{config.PROCESSES}:{command.id}', command.json())

    key = f'{config.PROCESS_DONE}:{command.id}'
    print(key)

    stdout_key = f'{config.LOGS}:{command.id}:stdout'
    stderr_key = f'{config.LOGS}:{command.id}:stderr'

    # TODO: iterate over logs here
    result = None

    print('loc 1')
    # while stdout_line or stderr_line or result is None:
    while result is None:
        pipeline = redis.pipeline()
        # pipeline.rpop(stdout_key)
        # pipeline.rpop(stderr_key)
        pipeline.rpop(stdout_key, line_buffer_size)
        pipeline.rpop(stderr_key, line_buffer_size)
        pipeline.rpop(key)
        stdout_line, stderr_line, result = pipeline.execute()

        if stdout_line:
            for line in stdout_line:
                print(line, end='')
        if stderr_line:
            for line in stderr_line:
                print(red(line), end='')

        # stdout_line = redis.rpop(stdout_key)
        # if stdout_line:
            # print(stdout_line, end='')
        # stderr_line= redis.rpop(stderr_key)
        # if stderr_line:
            # print(red(stderr_line), end='')
        # result = redis.rpop(key)

    read_rest_logs(redis, stdout_key, stderr_key)

    # _, message = redis.brpop(key)
    # result = ShellResult.parse_raw(message)
    result = ShellResult.parse_raw(result)
    # result.pprint()
    if result.returncode != 0:
        raise exceptions.ProcessResultError
    redis.delete(key)
    unlock_resources_semaphore(all_resources, redis)
    # redis.decr(os.environ['WEBHOOK_N_JOBS_KEY'])
    redis.hincrby(all_resources['job'].key, 'usage_current', -1)


if __name__ == '__main__':
    main()
