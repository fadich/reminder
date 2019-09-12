import json

from typing import Any

from aiohttp.web_response import Response


class TextResponse(Response):

    def __init__(self, text: Any, **kwargs):
        super().__init__(text=str(text), content_type='text/plain', **kwargs)


class JsonResponse(Response):

    def __init__(self, text: Any, **kwargs):
        super().__init__(text=json.dumps(text), content_type='application/json', **kwargs)
