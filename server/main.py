#!/usr/bin/env python3

import os
import sys
import argparse

import ws
import rest

from aiohttp.web import run_app

from reminder.web.utils import register_routes
from reminder.web.application import Application
from reminder.log import setup


def main():
    parser = argparse.ArgumentParser(description='run Reminder server')
    parser.add_argument('--host', dest='host', type=str, default='0.0.0.0', help='server host address')
    parser.add_argument('--port', dest='port', type=int, default=8000, help='server host port')
    args = parser.parse_args()

    setup(bool(os.environ.get('DEBUG', 1)))

    app = Application()
    app.add_routes(register_routes(ws))
    app.add_routes(register_routes(rest))

    run_app(app, host=args.host, port=args.port)

    return 0


if __name__ == '__main__':
    sys.exit(main())
