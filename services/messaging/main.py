#!/usr/bin/env python3

import sys

from reminder.web.application import Application

from handlers.reason import ReasonHandler


def main():
    app = Application('start Messaging service')
    app.route_table.add('/', ReasonHandler())
    app.run()

    return 0


if __name__ == '__main__':
    sys.exit(main())
