import abc

from typing import Iterable
from logging import getLogger
from bson.objectid import ObjectId

from reminder.orm import get_collection
from reminder.orm.fields import Field, ObjectIdField
from reminder.orm.exceptions import ValidationError


class Entity(object, metaclass=abc.ABCMeta):
    _id = ObjectIdField()
    _unique_fields = ()

    _values = {}

    def __init__(self, **kwargs):
        super().__init__()

        self._logger = getLogger(self.__class__.__name__.lower())

        for attr, value in kwargs.items():
            field = getattr(self.__class__, attr)
            if isinstance(field, Field):
                field._setup_field_name(attr)
            setattr(self, attr, value)

        if not self._is_unique():
            raise ValidationError('Not unique')

    @property
    def object_id(self):
        return self._id

    @property
    def logger(self):
        return self._logger

    @classmethod
    def get_collection(cls):
        return get_collection(cls.__name__.lower())

    def to_dict(self, exclude: Iterable = None):
        obj = {}
        for attr in self._values.keys():
            print('***' * 80)
            print(self._values)
            print(attr)
            print('***' * 80)
            if attr in exclude:
                continue
            if attr == '_id' and self.object_id:
                obj['_id'] = str(self.object_id)
                continue

            obj[attr] = getattr(self, attr)

        return obj

    def save(self):
        fields = self.to_dict(exclude=('_id', ))
        collection = self.__class__.get_collection()
        if self.object_id:
            collection.replace_one({'_id': self.object_id}, fields)
        else:
            getattr(self.__class__, '_id')._setup_field_name('_id')
            self._id = collection.insert_one(fields).inserted_id

    @classmethod
    def find_one(cls, criteria):
        fields = cls.get_collection().find_one(criteria)
        if not fields:
            return None

        return cls(**fields)

    @classmethod
    def find_by_id(cls, object_id: str):
        return cls.find_one({'_id': ObjectId(object_id)})

    def _is_unique(self):
        for fields in self._unique_fields:
            conditions = []
            for field in fields:
                conditions.append({
                    field: getattr(self, field)
                })

            criteria = {'$and': conditions}
            if self.object_id:
                criteria['$and'].append({
                    '_id': {
                        '$ne': self.object_id,
                    },
                })

            if self.get_collection().find_one(criteria):
                return False

        return True
