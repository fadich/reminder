#!/usr/bin/env python3

import sys

from reminder.web.application import Application

from handlers import SignUpHandler, SignInHandler


def main():
    app = Application('start Authorization service')
    app.route_table.add('/sign-up', SignUpHandler(), http_method='post')
    app.route_table.add('/sign-in', SignInHandler(), http_method='post')
    app.run()

    return 0


if __name__ == '__main__':
    sys.exit(main())
