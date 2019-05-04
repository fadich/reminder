from typing import Any

from reminder.web.errors import AuthenticationError
from reminder.web.validation import FieldsValidator
from reminder.web.handlers import WebSocketHandler, WebSocketResponse

from .reason_maintainers import ReasonMessageMaintainer


class ReasonHandler(WebSocketHandler, ReasonMessageMaintainer):

    async def _authenticate(self, request):
        client_id = request.query.get('id')
        if not client_id:
            raise AuthenticationError('Invalid client ID')

        return client_id

    async def on_message(self, data: Any, ws: WebSocketResponse):
        if not isinstance(data, dict):
            return

        validator = FieldsValidator()
        validator.add_rules({
            'reason': [
                (FieldsValidator.VALIDATE_REQUIRED, 'No reason specified'),
                (FieldsValidator.VALIDATE_TYPE_STRING, 'Invalid reason format'),
                (lambda f: hasattr(self, reason_handler), f'Unknown reason "{data.get("reason")}"'),
            ],
            'data': [],
        })
        validator.load_data(data)
        reason_handler = f'on_reason_{validator.fields.get("reason")}'

        if not validator.is_valid():
            await ws.send_json({
                'error': validator.errors
            })
            return

        method = getattr(self, reason_handler)
        await method(validator.fields.get('data'), ws)

    async def on_auth_failed(self, ws: WebSocketResponse):
        await ws.send_json({
            'error': 'Invalid client ID'
        })

    async def on_connect(self, ws: WebSocketResponse):
        print(self.connections)

    async def on_disconnect(self, ws: WebSocketResponse):
        print(self.connections)
