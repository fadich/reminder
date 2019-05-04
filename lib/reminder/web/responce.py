from aiohttp.web import WebSocketResponse as WSResponseBase


class WebSocketResponse(WSResponseBase):

    def __str__(self):
        return '{}'.format(id(self))

    def __eq__(self, other):
        """Identify client responses for correctly removing/closing etc."""
        return id(self) == id(other)
