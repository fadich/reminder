from reminder.web.router import route_table

from .handlers.home import HomeHandler
from .handlers.room import CreateRoomHandler


route_table.add('/', HomeHandler(), method='get')
route_table.add('/room/create', CreateRoomHandler(), method='post')
