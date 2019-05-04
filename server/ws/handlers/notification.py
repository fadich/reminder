from typing import Any

from reminder.web.handlers import WebSocketHandler


class NotificationHandler(WebSocketHandler):

    async def on_message(self, data: Any):
        pass
