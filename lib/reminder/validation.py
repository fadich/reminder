from typing import Dict, List, Tuple, Any, Iterable


class Validator(object):

    def __init__(self):
        self._errors: Dict[str, str] = {}

    @property
    def errors(self):
        return self._errors

    def add_error(self, field: str, message: str):
        self._errors[field] = message

    def has_errors(self):
        return bool(self.errors.keys())

    def clean_errors(self):
        self._errors = {}

    @staticmethod
    def validate_required(value, *args, **kwargs):
        return value is not None

    @staticmethod
    def validate_type_int(value, *args, **kwargs):
        return isinstance(value, int)

    @staticmethod
    def validate_type_float(value, *args, **kwargs):
        return isinstance(value, float)

    @staticmethod
    def validate_type_number(value, *args, **kwargs):
        return Validator.validate_type_float(value) or Validator.validate_type_int(value)

    @staticmethod
    def validate_type_string(value, *args, **kwargs):
        return isinstance(value, str)

    @staticmethod
    def validate_type_list(value, *args, **kwargs):
        return isinstance(value, list)

    @staticmethod
    def validate_type_dict(value, *args, **kwargs):
        return isinstance(value, dict)


class FieldsValidator(Validator):
    VALIDATE_REQUIRED = (Validator.validate_required, 'should not be empty')
    VALIDATE_TYPE_INT = (Validator.validate_type_int, 'should be an integer')
    VALIDATE_TYPE_FLOAT = (Validator.validate_type_float, 'should be a floating point number')
    VALIDATE_TYPE_NUMBER = (Validator.validate_type_number, 'should be a number')
    VALIDATE_TYPE_STRING = (Validator.validate_type_string, 'should be a string')
    VALIDATE_TYPE_LIST = (Validator.validate_type_list, 'should be a list')
    VALIDATE_TYPE_DICT = (Validator.validate_type_dict, 'should be an object')

    def __init__(self):
        super().__init__()
        self._rules = {}
        self._fields = {}

    @property
    def validation_rules(self) -> Dict[str, List]:
        return self._rules

    @property
    def fields(self) -> Dict[str, Any]:
        return self._fields

    def add_rules(self, rules: Dict[str, List[Tuple]]):
        """Example:
        {
            'field_name': [
                FieldsValidationHandler.VALIDATE_REQUIRED,
                FieldsValidationHandler.VALIDATE_TYPE_DICT,
            ]
        }
        """
        self._rules = rules

    def load_data(self, fields: Dict[str, Any]):
        self.clean_errors()
        self._fields = dict(fields)

    def validate(self, fields: Iterable = None):
        fields = fields or self.fields.keys()

        for field, rules in self.validation_rules.items():
            for rule in rules:
                if rule[0] == FieldsValidator.VALIDATE_REQUIRED[0] and field not in fields:
                    self.add_error(field, rule[1])

        for field in fields:
            if field not in self.validation_rules:
                self.add_error(field, 'Unexpected field')
                continue
            for is_valid, error in self.validation_rules[field]:
                if not is_valid(self.fields[field], field):
                    self.add_error(field, error)

    def is_valid(self):
        self.validate()
        return not self.has_errors()
