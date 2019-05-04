import abc
import json

from typing import Any
from logging import getLogger

from asyncio import (
    run_coroutine_threadsafe,
    get_event_loop,
    Queue,
    sleep,
)

from aiohttp.web_request import Request
from aiohttp.web_response import StreamResponse
from aiohttp.http_websocket import WSMessage, WSMsgType

from .responce import WebSocketResponse


logger = getLogger(__name__)


class Handler(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    async def __call__(self, request: Request) -> StreamResponse:
        pass


class RestHandler(Handler, metaclass=abc.ABCMeta):
    pass


class WebSocketHandler(Handler, metaclass=abc.ABCMeta):

    def __init__(self):
        super().__init__()

        self.ws: WebSocketResponse = None

        self.message_queue = Queue()
        self.loop = get_event_loop()

        self._connections = {}

    async def __call__(self, request: Request):
        self.ws = WebSocketResponse()
        await self.ws.prepare(request)
        await self.on_connect()

        run_coroutine_threadsafe(self._write_message(), self.loop)
        await self._read_message()

        await self.on_disconnect()

        return self.ws

    @abc.abstractmethod
    async def on_message(self, data: Any):
        pass

    @property
    def connections(self):
        return self._connections

    async def send_message(self, msg: dict):
        await self.message_queue.put(msg)

    async def on_connect(self):
        logger.info(f'<{self.ws}> connected')

        logger.debug(self.connections)

        if not isinstance(self._connections.get(str(self.ws)), list):
            self._connections[str(self.ws)] = []

        self._connections.get(str(self.ws)).append(self.ws)

        logger.debug(self.connections)

    async def on_disconnect(self):
        logger.debug(self.connections)
        logger.info(f'<{self.ws}> disconnected')

        self._connections.get(str(self.ws)).remove(self.ws)
        if not len(self._connections.get(str(self.ws))):
            del self._connections[str(self.ws)]

        logger.debug(self.connections)

    async def _write_message(self):
        while not self.ws.closed:
            await sleep(0.001)
            if self.message_queue.empty():
                continue

            msg = await self.message_queue.get()
            await self.ws.send_json(msg)

    async def _read_message(self):
        async for msg in self.ws:
            await self._handle_message(msg)
            await sleep(0.001)

    async def _handle_message(self, msg: WSMessage):
        if msg.type != WSMsgType.TEXT:
            logger.warning(f'ws message type is {msg.type}')
            return

        try:
            data = json.loads(msg.data)
        except json.JSONDecodeError:
            await self.ws.send_json({'error': 'invalid json format'})
            return

        await self.on_message(data)
