from typing import Any

from reminder.web.handlers import WebSocketResponse


class ReasonMessageMaintainer(object):

    async def on_reason_message(self, data: Any, ws: WebSocketResponse):
        await ws.send_json({
            'answer': data
        })
