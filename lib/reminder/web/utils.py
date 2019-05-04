from aiohttp.web_routedef import RouteTableDef

from reminder.web.router import RouteTable


__all__ = [
    'register_routes',
]


def register_routes(module) -> RouteTableDef:
    route_table_attr = 'route_table'
    if not hasattr(module, route_table_attr):
        raise AttributeError(f'Module "{module.__name__}" has no attribute "{route_table_attr}". '
                             f'Expected "{route_table_attr}" as an instance of <{RouteTable}>')

    return getattr(module, route_table_attr).table_def
