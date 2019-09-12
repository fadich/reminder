import abc

from typing import Any

from reminder.web.handlers import Handler
from reminder.validation import FieldsValidator
from reminder.web.rest.response import JsonResponse, TextResponse


class RestHandler(Handler, metaclass=abc.ABCMeta):

    def send_text(self, response: Any, status: int = 200, **kwargs) -> TextResponse:
        return TextResponse(text=response, status=status, **kwargs)

    def send_json(self, response: Any, status: int = 200, **kwargs) -> JsonResponse:
        return JsonResponse(text=response, status=status, **kwargs)

    def send_success_json(self, response: Any, status: int = 200, **kwargs) -> JsonResponse:
        return self.send_json({
            'success': response
        }, status=status, **kwargs)

    def send_error_json(self, response: Any, status: int = 200, **kwargs) -> JsonResponse:
        return self.send_json({
            'error': response
        }, status=status, **kwargs)


class ValidationHandler(RestHandler, metaclass=abc.ABCMeta):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._validator = FieldsValidator()
        self._validator.add_rules(self.rules)

    @property
    def validator(self):
        return self._validator

    @property
    @abc.abstractmethod
    def rules(self) -> dict:
        pass
    
    async def __call__(self, request):
        await self.prepare(request)
        if not self.validator.is_valid():
            return self.validation_error_response()

        return await self.handle(request)

    async def prepare(self, request):
        await super().prepare(request)
        self.validator.load_data(self.request_data)

    def validation_error_response(self):
        return self.send_json({
            'status': 'error',
            'errors': self.validator.errors,
        }, status=400)
