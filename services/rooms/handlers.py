import json

from traceback import format_exc

from aiohttp.web_request import Request
from aiohttp.web_response import StreamResponse

from reminder.web.rest.handlers import ValidationHandler
from reminder.web.validation import FieldsValidator

from orm.models import Room


class CreateRoomHandler(ValidationHandler):
    rooms = {}

    def rules(self) -> dict:
        return {
            'name': [
                (FieldsValidator.VALIDATE_REQUIRED, 'No name set'),
                (FieldsValidator.VALIDATE_TYPE_STRING, 'String type expected'),
            ],
            'clients': [
                (FieldsValidator.VALIDATE_REQUIRED, 'No clients set'),
                (FieldsValidator.VALIDATE_TYPE_LIST, 'List expected'),
                (lambda field: all(isinstance(client, str) for client in field), 'Client ID should be a string'),
            ]
        }

    async def __call__(self, request: Request) -> StreamResponse:
        data = dict(await request.post())
        self.logger.debug(data)
        for key, value in data.items():
            try:
                dumed = json.loads(data[key])
                if isinstance(dumed, list) or isinstance(dumed, dict):
                    data[key] = dumed
            except json.JSONDecodeError as e:
                self.logger.warning(format_exc())

        self.validator.load_data(data)
        if not self.validator.is_valid():
            self.logger.debug(self.validator.fields)
            return self.validation_error_response()

        room = Room()
        room.name = self.validator.fields['name']
        room.members = self.validator.fields['clients']

        return self.send_json({
            'status': 'success',
            'data': {
                'room_id': 1,
            },
        })
