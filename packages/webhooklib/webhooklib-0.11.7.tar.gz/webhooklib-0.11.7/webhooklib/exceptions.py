class ProcessCreateError(Exception):
    pass


class ProcessResultError(Exception):
    pass


class CmdNotFoundError(FileNotFoundError):
    pass


class CwdNotFoundError(FileNotFoundError):
    pass
