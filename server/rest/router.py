from reminder.web.router import route_table

from .handlers.home import HomeHandler


route_table.add('/', HomeHandler(), method='get')
