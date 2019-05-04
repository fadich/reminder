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
    def validate_required(field):
        return field is not None

    @staticmethod
    def validate_type_int(field):
        return isinstance(field, int)

    @staticmethod
    def validate_type_float(field):
        return isinstance(field, float)

    @staticmethod
    def validate_type_number(field):
        return Validator.validate_type_float(field) or Validator.validate_type_int(field)

    @staticmethod
    def validate_type_string(field):
        return isinstance(field, str)

    @staticmethod
    def validate_type_list(field):
        return isinstance(field, list)

    @staticmethod
    def validate_type_dict(field):
        return isinstance(field, dict)


class FieldsValidator(Validator):
    VALIDATE_REQUIRED = Validator.validate_required
    VALIDATE_TYPE_INT = Validator.validate_type_int
    VALIDATE_TYPE_FLOAT = Validator.validate_type_float
    VALIDATE_TYPE_NUMBER = Validator.validate_type_number
    VALIDATE_TYPE_STRING = Validator.validate_type_string
    VALIDATE_TYPE_LIST = Validator.validate_type_list
    VALIDATE_TYPE_DICT = Validator.validate_type_dict

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
                (FieldsValidationHandler.VALIDATE_REQUIRED, 'This field is required'),
                (FieldsValidationHandler.VALIDATE_TYPE_DICT, 'Invalid field type'),
            ]
        }
        """
        self._rules = rules

    def load_data(self, fields: Dict[str, Any]):
        self.clean_errors()
        self._fields = dict(fields)

    def validate(self, fields: Iterable = None):
        fields = fields or self.fields.keys()

        for rule_field, rules in self.validation_rules.items():
            for rule in rules:
                if rule[0] == FieldsValidator.VALIDATE_REQUIRED and rule_field not in fields:
                    self.add_error(rule_field, rule[1])

        for field in fields:
            if field not in self.validation_rules:
                self.add_error(field, 'Unexpected field')
                continue
            for is_valid, error in self.validation_rules[field]:
                if not is_valid(self.fields[field]):
                    self.add_error(field, error)
                    break

    def is_valid(self):
        self.validate()
        return not self.has_errors()
