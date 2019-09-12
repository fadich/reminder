from aiohttp.web import WebSocketResponse as WSResponseBase


class WebSocketResponse(WSResponseBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._client_id: str = None

    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, value: str):
        if self.client_id is None:
            self._client_id = value
            return
        raise ValueError('Client ID is already set')

    def __str__(self):
        return '{}'.format(id(self))

    def __eq__(self, other):
        """Identify client responses for correctly removing/closing etc."""
        return id(self) == id(other)
