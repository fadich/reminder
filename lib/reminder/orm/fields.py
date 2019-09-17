from abc import ABCMeta
from bson.objectid import ObjectId

from reminder.validation import FieldsValidator
from reminder.orm.exceptions import ValidationError


class Field(object, metaclass=ABCMeta):

    def __init__(self, required=False, _field_name: str = None):
        rules = {'value': self._validation_rules}
        if required:
            rules['value'].append(FieldsValidator.VALIDATE_REQUIRED)

        self._validator = FieldsValidator()
        self._validator.add_rules(rules)

        self._field_name = None
        if _field_name:
            self._field_name = _field_name

    def get_value(self, entity):
        return entity._values.get(self._field_name)

    def set_value(self, entity, value):
        self._validator.load_data({'value': value})
        self._validator.validate()
        if not self._validator.is_valid():
            raise ValidationError(f'Invalid value {self._validator.errors}')

        entity._values[self._field_name] = value

    def delete_value(self, entity):
        if self._field_name in entity._values:
            del entity._values[self._field_name]

    def __get__(self, instance, owner):
        if instance:
            return self.get_value(instance)
        return self

    def __set__(self, instance, value):
        self.set_value(instance, value)

    def __delete__(self, instance):
        return self.delete_value(instance)

    def _setup_field_name(self, field_name):
        if self._field_name is None:
            self._field_name = field_name

    @property
    def _validation_rules(self):
        return []


class ObjectIdField(Field):

    @property
    def _validation_rules(self):
        return [
            (
                lambda v, *args, **kwargs: isinstance(v, ObjectId),
                f'Must be instance of {ObjectId.__name__}'
            ),
        ]


class IntegerField(Field):

    @property
    def _validation_rules(self):
        return [
            FieldsValidator.VALIDATE_TYPE_INT,
        ]


class FloatField(Field):

    @property
    def _validation_rules(self):
        return [
            FieldsValidator.VALIDATE_TYPE_FLOAT,
        ]


class StringField(Field):

    @property
    def _validation_rules(self):
        return [
            FieldsValidator.VALIDATE_TYPE_STRING,
        ]
