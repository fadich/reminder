from reminder.web.router import route_table

from .handlers.reason import ReasonHandler

notification_handler = ReasonHandler()

route_table.add('/ws', notification_handler)
