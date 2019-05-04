from typing import Any

from reminder.web.errors import AuthenticationError
from reminder.web.handlers import WebSocketHandler, WebSocketResponse


class NotificationHandler(WebSocketHandler):

    async def _authenticate(self, request):
        client_id = request.query.get('id')
        if not client_id:
            raise AuthenticationError('Invalid client ID')

        return client_id

    async def on_message(self, data: Any):
        pass

    async def on_auth_failed(self, ws: WebSocketResponse):
        await ws.send_json({
            'error': 'Invalid client ID'
        })

    async def on_connect(self, ws: WebSocketResponse):
        print(self.connections)

    async def on_disconnect(self, ws: WebSocketResponse):
        print(self.connections)
