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
from aiohttp.http_websocket import WSMessage, WSMsgType
from aiohttp.web_response import StreamResponse

from .validation import Validator
from .errors import AuthenticationError
from .responce import WebSocketResponse, JsonResponse

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


class RestHandler(Handler, metaclass=abc.ABCMeta):

    def send_json(self, response: Any, status: int = 200, **kwargs) -> JsonResponse:
        return JsonResponse(text=json.dumps(response), status=status, **kwargs)


class RestValidationHandler(RestHandler, metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def validator(self) -> Validator:
        pass

    def validation_error_response(self):
        return self.send_json({
            'status': 'error',
            'errors': self.validator.errors,
        }, status=400)


class WebSocketHandler(Handler, metaclass=abc.ABCMeta):

    def __init__(self):
        super().__init__()

        self._message_queue = Queue()
        self._loop = get_event_loop()

        self._connections: Dict[str, List[WebSocketResponse]] = {}

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
    async def _authenticate(self, request: Request) -> str:
        """Should returns request"""
        pass

    @abc.abstractmethod
    async def on_message(self, data: Any, ws: WebSocketResponse):
        """On message received"""
        pass

    async def on_auth_failed(self, ws: WebSocketResponse):
        """On authorization failed, before disconnecting"""
        pass

    async def on_connect(self, ws: WebSocketResponse):
        """Post connection (on success auth)"""
        pass

    async def on_disconnect(self, ws: WebSocketResponse):
        """Pre disconnection (for last will message, for example)"""
        pass

    async def __call__(self, request: Request):
        ws = WebSocketResponse()
        request = request
        await ws.prepare(request)

        try:
            client_id = await self._authenticate(request)
            if not client_id:
                raise AuthenticationError()
        except AuthenticationError:
            await self.on_auth_failed(ws)
            return ws

        await self._append_client(client_id, ws)
        await self.on_connect(ws)

        run_coroutine_threadsafe(self._write_message(ws), self.loop)
        await self._read_message(ws)

        await self.on_disconnect(ws)
        await self._remove_client(client_id, ws)

        return ws

    async def send_message(self, msg: dict, client_id: str):
        await self.message_queue.put({
            'client_id': client_id,
            'data': msg
        })

    async def _append_client(self, client_id: str, ws: WebSocketResponse):
        if not isinstance(self.connections.get(client_id), list):
            self.connections[client_id] = []

        self.connections.get(client_id).append(ws)

    async def _remove_client(self, client_id: str, ws: WebSocketResponse):
        self.connections.get(client_id).remove(ws)
        if not len(self.connections.get(client_id)):
            del self.connections[client_id]

    async def _write_message(self, ws: WebSocketResponse):
        while not ws.closed:
            await sleep(0.001)
            if self.message_queue.empty():
                continue

            msg = await self.message_queue.get()  # type: dict
            clients = self.connections.get(msg.get('client_id'))

            for client in clients:
                run_coroutine_threadsafe(client.send_json(msg.get('data')), get_event_loop())

    async def _read_message(self, ws: WebSocketResponse):
        async for msg in ws:
            await self._handle_message(msg, ws)
            await sleep(0.001)

    async def _handle_message(self, msg: WSMessage, ws: WebSocketResponse):
        if msg.type != WSMsgType.TEXT:
            logger.warning(f'ws message type is {msg.type}')
            return

        try:
            data = json.loads(msg.data)
        except json.JSONDecodeError:
            await ws.send_json({'error': 'invalid json format'})
            return

        await self.on_message(data, ws)
