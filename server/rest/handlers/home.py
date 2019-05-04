from logging import getLogger
from asyncio import run_coroutine_threadsafe, get_event_loop

from aiohttp.web import Response

from reminder.web.handlers import RestHandler

from ws import notification_handler


logger = getLogger(__name__)


class HomeHandler(RestHandler):

    async def __call__(self, request):
        q = request.query.get('q')

        if len(notification_handler.active_clients):
            for client in notification_handler.active_clients:
                run_coroutine_threadsafe(
                    notification_handler.send_message({'Hello': q}, client),
                    get_event_loop())
            return Response(text='Hello!')

        return Response(text='No connections')
