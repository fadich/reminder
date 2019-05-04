from typing import Any

from aiohttp.web_response import Response
from aiohttp.web import WebSocketResponse as WSResponseBase


class WebSocketResponse(WSResponseBase):

    def __str__(self):
        return '{}'.format(id(self))

    def __eq__(self, other):
        """Identify client responses for correctly removing/closing etc."""
        return id(self) == id(other)


class JsonResponse(Response):

    def __init__(self, text: Any, **kwargs):
        super().__init__(text=text, content_type='application/json', **kwargs)
