#!/usr/bin/env python3

import sys

from reminder.web.application import Application

from handlers import HomeHandler


def main():
    app = Application('start Homepage service')
    app.route_table.add('/', HomeHandler(), http_method='get')
    app.run()

    return 0


if __name__ == '__main__':
    sys.exit(main())
