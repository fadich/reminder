from aiohttp.web_routedef import RouteTableDef

from reminder.web.handlers import Handler
from reminder.functional.decorators import cashed_property


ALLOWED_METHODS = ('head', 'get', 'post', 'patch', 'put', 'delete')


class RouteTable(object):

    def __init__(self):
        self._route_table_def = RouteTableDef()

    def add(self, path: str, handler: Handler, http_method: str = 'get'):
        http_method = http_method.lower()

        if http_method not in ALLOWED_METHODS:
            raise AssertionError(f'Unknown method "{http_method}"')

        if not isinstance(handler, Handler):
            raise AssertionError(f'Handler should be instance of "{Handler}", "{handler.__class__}" given')

        """The structure is `route_table_def -> http_method -> path -> handler`"""
        method = getattr(self._route_table_def, http_method)
        route_register = method(path)
        route_register(handler)

    @property
    def table_def(self):
        return self._route_table_def


@cashed_property()
def route_table():
    return RouteTable()
