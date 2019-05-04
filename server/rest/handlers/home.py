from logging import getLogger

from aiohttp.web import Response

from reminder.web.handlers import RestHandler

from ws import notification_handler


logger = getLogger(__name__)


class HomeHandler(RestHandler):

    async def __call__(self, request):
        q = request.query.get('q')

        if len(notification_handler.connections.keys()):
            await notification_handler.send_message({'Hello': q})
            return Response(text='Hello!')

        return Response(text='No connections')
