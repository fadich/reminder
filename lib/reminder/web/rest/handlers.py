import abc
import json

from typing import Any
from logging import getLogger

from reminder.web.handlers import Handler
from reminder.web.validation import FieldsValidator
from reminder.web.rest.response import JsonResponse


logger = getLogger(__name__)


class RestHandler(Handler, metaclass=abc.ABCMeta):

    def send_json(self, response: Any, status: int = 200, **kwargs) -> JsonResponse:
        return JsonResponse(text=json.dumps(response), status=status, **kwargs)


class ValidationHandler(RestHandler, metaclass=abc.ABCMeta):

    @property
    def validator(self):
        validator = FieldsValidator()
        validator.add_rules(self.rules)

        return validator

    @property
    @abc.abstractmethod
    def rules(self) -> dict:
        pass

    def validation_error_response(self):
        return self.send_json({
            'status': 'error',
            'errors': self.validator.errors,
        }, status=400)
