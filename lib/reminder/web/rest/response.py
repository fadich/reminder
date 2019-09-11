from typing import Any

from aiohttp.web_response import Response


class TextResponse(Response):
    pass


class JsonResponse(Response):

    def __init__(self, text: Any, **kwargs):
        super().__init__(text=text, content_type='application/json', **kwargs)
