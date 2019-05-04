import sys

from logging import (
    INFO,
    DEBUG,
    NOTSET,
    WARNING,
    Filter,
    basicConfig,
    StreamHandler,
)


class MaxLevelFilter(Filter):

    def __init__(self, max_level: int):
        super().__init__()
        self.max_level = max_level

    def filter(self, record):
        return record.levelno < self.max_level


class CommonStdHandler(StreamHandler):

    def __init__(self):
        super().__init__(stream=sys.stdout)
        self.setLevel(NOTSET)
        self.addFilter(MaxLevelFilter(WARNING))


class ErrorStdHandler(StreamHandler):

    def __init__(self):
        super().__init__(stream=sys.stderr)
        self.setLevel(WARNING)


def setup(debug: bool = False):
    basicConfig(level=DEBUG if debug else INFO, handlers=[
        CommonStdHandler(),
        ErrorStdHandler(),
    ])
