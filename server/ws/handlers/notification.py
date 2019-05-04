from typing import Any

from reminder.web.handlers import WebSocketHandler
from reminder.web.errors import AuthenticationError


class NotificationHandler(WebSocketHandler):

    async def _authenticate(self):
        client_id = self.request.query.get('id')
        if not client_id:
            raise AuthenticationError('Invalid client ID')

        self._client_id = client_id

    async def on_message(self, data: Any):
        pass

    async def on_auth_failed(self):
        await self.ws.send_json({
            'error': 'Invalid client ID'
        })

    async def on_connect(self):
        print(self.connections)
