#!/usr/bin/env python3

import sys

from reminder.web.application import Application

from handlers import CreateRoomHandler


def main():
    app = Application('start Rooms service')
    app.route_table.add('/', CreateRoomHandler(), http_method='post')
    app.run()

    return 0


if __name__ == '__main__':
    sys.exit(main())
