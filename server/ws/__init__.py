from reminder.web.router import route_table

from .handlers.notification import NotificationHandler

notification_handler = NotificationHandler()

route_table.add('/ws', notification_handler)
