import abc

from logging import getLogger

from aiohttp.web_request import Request
from aiohttp.web_response import StreamResponse


logger = getLogger(__name__)


class Handler(object, metaclass=abc.ABCMeta):

    def __init__(self):
        self._logger = getLogger(self.__class__.__name__)

    @property
    def logger(self):
        return self._logger

    @abc.abstractmethod
    async def __call__(self, request: Request) -> StreamResponse:
        pass
