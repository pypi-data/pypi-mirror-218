REDIS_PREFIX = 'webhooklib'
PROCESS_DONE = f'{REDIS_PREFIX}:process_done'
PROCESSES = f'{REDIS_PREFIX}:processes'
LOGS = f'{REDIS_PREFIX}:logs'
LOGS_TTL = 60 * 60 * 24 * 7  # 7 days
