import abc

from logging import getLogger
from bson.objectid import ObjectId

from reminder.orm import get_collection
from reminder.validation import FieldsValidator
from reminder.orm.exceptions import ValidationError


class Entity(object, metaclass=abc.ABCMeta):

    def __init__(self, **kwargs):
        super().__init__()

        self._id = None  # type: ObjectId
        self._logger = getLogger(self.__class__.__name__.lower())

        self._validator = FieldsValidator()
        self._validator.add_rules(self.get_rules())
        self._validator.load_data(kwargs)

    @property
    def object_id(self):
        return self._id

    @property
    def logger(self):
        return self._logger

    @property
    def validator(self):
        return self._validator

    @classmethod
    def get_collection(cls):
        return get_collection(cls.__name__.lower())

    @classmethod
    def get_rules(cls):
        return {}

    def __getattr__(self, item):
        return self.validator.fields.get(item)

    def to_dict(self, skip_id=False):
        obj = {}
        for field in self.get_rules():
            obj[field] = getattr(self, field)

        if not skip_id:
            obj['_id'] = str(self.object_id) if self.object_id else None

        return obj

    def save(self):
        if not self.validator.is_valid():
            raise ValidationError(self.validator.errors)

        fields = self.to_dict(True)
        collection = self.__class__.get_collection()
        if self.object_id:
            collection.replace_one({'_id': self.object_id}, fields)
        else:
            self._id = collection.insert_one(fields).inserted_id

    @classmethod
    def find_one(cls, criteria):
        fields = cls.get_collection().find_one(criteria)
        if not fields:
            return None

        _id = fields.pop('_id')
        user = cls(**fields)
        user._id = _id

        return user

    @classmethod
    def find_by_id(cls, object_id: str):
        return cls.find_one({'_id': ObjectId(object_id)})


def validate_unique(entity: Entity, error: str = 'already exists'):
    def is_valid(value, field_name: str):
        fields = entity.find_one({field_name: value})
        return not bool(fields)

    return is_valid, error
