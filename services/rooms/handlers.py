from aiohttp.web_request import Request
from aiohttp.web_response import StreamResponse

from reminder.validation import FieldsValidator
from reminder.web.rest.handlers import ValidationHandler

from orm.models import Room


class CreateRoomHandler(ValidationHandler):
    rooms = {}

    def rules(self) -> dict:
        return {
            'name': [
                FieldsValidator.VALIDATE_REQUIRED,
                FieldsValidator.VALIDATE_TYPE_STRING,
            ],
            'clients': [
                FieldsValidator.VALIDATE_REQUIRED,
                FieldsValidator.VALIDATE_TYPE_LIST,
                (
                    lambda field, *args, **kwargs: all(isinstance(client, str) for client in field),
                    'Client ID should be a string'
                ),
            ]
        }

    async def handle(self, request: Request) -> StreamResponse:
        room = Room()
        room.name = self.validator.fields['name']
        room.members = self.validator.fields['clients']

        return self.send_json({
            'status': 'success',
            'data': {
                'room_id': 1,
            },
        })
