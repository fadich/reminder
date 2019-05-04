import abc
import json

from typing import Any, List, Dict
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

from .errors import AuthenticationError
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

        self._client_id: str = None
        self._request: Request = None
        self._ws: WebSocketResponse = None

        self._message_queue = Queue()
        self._loop = get_event_loop()

        self._connections: Dict[str, List[WebSocketResponse]] = {}

    @property
    def client_id(self):
        return self._client_id

    @property
    def request(self):
        return self._request

    @property
    def ws(self):
        return self._ws

    @property
    def message_queue(self):
        return self._message_queue

    @property
    def loop(self):
        return self._loop

    @property
    def connections(self):
        return self._connections

    @property
    def active_clients(self):
        return tuple(self.connections.keys())

    @abc.abstractmethod
    async def _authenticate(self):
        """Should set self._client_id"""
        pass

    @abc.abstractmethod
    async def on_message(self, data: Any):
        pass

    async def on_auth_failed(self):
        pass

    async def on_connect(self):
        pass

    async def on_disconnect(self):
        pass

    async def __call__(self, request: Request):
        self._ws = WebSocketResponse()
        self._request = request
        await self.ws.prepare(self.request)

        try:
            await self._authenticate()
            if not self.client_id:
                raise AuthenticationError()
        except AuthenticationError:
            await self.on_auth_failed()
            return self.ws

        await self._append_client()
        await self.on_connect()

        run_coroutine_threadsafe(self._write_message(), self.loop)
        await self._read_message()

        await self.on_disconnect()
        await self._remove_client()

        return self.ws

    async def send_message(self, msg: dict, client_id: str):
        await self.message_queue.put({
            'client_id': client_id,
            'data': msg
        })

    async def _append_client(self):
        if not isinstance(self._connections.get(self.client_id), list):
            self._connections[self.client_id] = []

        self._connections.get(self.client_id).append(self.ws)

    async def _remove_client(self):
        self._connections.get(self.client_id).remove(self._ws)
        if not len(self._connections.get(self.client_id)):
            del self._connections[self.client_id]

    async def _write_message(self):
        while not self.ws.closed:
            await sleep(0.001)
            if self.message_queue.empty():
                continue

            msg = await self.message_queue.get()  # type: dict
            clients = self.connections.get(msg.get('client_id'))

            for client in clients:
                run_coroutine_threadsafe(client.send_json(msg.get('data')), get_event_loop())

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
