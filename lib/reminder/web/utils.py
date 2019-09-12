from argparse import ArgumentParser


__all__ = [
    'get_server_argument_parser',
]


def get_server_argument_parser(description: str = None, parser: ArgumentParser = None):
    if not parser:
        parser = ArgumentParser(description=description)
    elif description:
        parser.description = description

    parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='set debug log level')
    parser.add_argument('--host', dest='host', type=str, default='0.0.0.0', help='server host address')
    parser.add_argument('--port', dest='port', type=int, default=8000, help='server host port')

    return parser
