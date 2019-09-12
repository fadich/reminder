from reminder.web.rest.handlers import RestHandler
from reminder.web.rest.response import TextResponse


class HomeHandler(RestHandler):

    async def handle(self, request):
        q = request.query.get('q')
        if q:
            return TextResponse(text=f'You said "{q}"')

        return TextResponse(text='Specify the `q` GET-parameter value')
