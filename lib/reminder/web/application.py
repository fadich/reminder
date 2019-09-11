import os

from aiohttp.web import Application as BaseApp, run_app

from reminder import log
from reminder.web.router import route_table
from reminder.web.utils import get_server_argument_parser


class Application(object):

    def __init__(self, description: str = None, argument_parser=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.application = BaseApp()
        self._argument_parser = get_server_argument_parser(description, argument_parser)

    @property
    def route_table(self):
        return route_table

    @property
    def argument_parser(self):
        return self._argument_parser

    def run(self, host: str = None, port: int = None, debug: bool = False):
        args = self.argument_parser.parse_args()

        host = host or args.host
        port = port or args.port
        if args.debug is not None:
            debug = args.debug
        elif os.environ.get('DEBUG') is not None:
            debug = os.environ.get('DEBUG')

        self.application.add_routes(self.route_table.table_def)

        log.setup(debug=debug)
        return run_app(self.application, host=host, port=port)
