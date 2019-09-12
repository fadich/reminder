import abc

from logging import getLogger

from aiohttp.web_request import Request
from aiohttp.web_response import StreamResponse


class Handler(object, metaclass=abc.ABCMeta):

    def __init__(self):
        self._logger = getLogger(self.__class__.__name__)
        self._request_data = {}

    @property
    def logger(self):
        return self._logger

    @property
    def request_data(self):
        return self._request_data

    @abc.abstractmethod
    async def handle(self, request):
        pass

    async def __call__(self, request) -> StreamResponse:
        await self.prepare(request)
        return await self.handle(request)

    async def prepare(self, request):
        self._request_data = await self._load_data(request)

    async def _load_data(self, request):
        data = {}
        if request.can_read_body:
            data = await request.json()

        return data
