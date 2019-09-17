from reminder.orm.entity import Entity
from reminder.orm.fields import StringField


class User(Entity):
    login = StringField(required=True)
    password = StringField(required=True)

    _unique_fields = (
        ('login', ),
    )
