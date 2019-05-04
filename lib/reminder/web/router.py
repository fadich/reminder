from aiohttp.web_routedef import RouteTableDef

from reminder.web.handlers import Handler
from reminder.functional.decorators import CashedProperty


ALLOWED_METHODS = ('head', 'get', 'post', 'patch', 'put', 'delete')


class RouteTable(object):

    def __init__(self):
        self._route_table = RouteTableDef()

    def add(self, path: str, handler: Handler, method: str = 'get'):
        method = method.lower()

        if method not in ALLOWED_METHODS:
            raise AssertionError(f'Unknown method "{method}"')
        if not isinstance(handler, Handler):
            raise AssertionError(f'Handler should be instance of "{Handler}", "{handler.__class__}" given')

        attr = getattr(self._route_table, method)
        func = attr(path)
        func(handler)

    @property
    def table_def(self):
        return self._route_table


@CashedProperty()
def route_table():
    return RouteTable()
