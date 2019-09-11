from logging import getLogger

from reminder.web.rest.handlers import RestHandler
from reminder.web.rest.response import TextResponse

logger = getLogger(__name__)


class HomeHandler(RestHandler):

    async def __call__(self, request):
        q = request.query.get('q')
        if q:
            return TextResponse(text=f'You said "{q}"')

        return TextResponse(text='You did not say something. Get the `q` parameter value')
