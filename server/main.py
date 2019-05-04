import os

import ws
import rest

from aiohttp.web import run_app

from reminder.web.utils import register_routes
from reminder.web.application import Application
from reminder.log import setup


setup(bool(os.environ.get('DEBUG', 1)))

app = Application()
app.add_routes(register_routes(ws))
app.add_routes(register_routes(rest))

run_app(app, port=8000)
