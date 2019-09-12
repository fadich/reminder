from reminder.validation import FieldsValidator
from reminder.orm.entity import Entity, validate_unique
from reminder.security.password import hash_password, verify_password


class User(Entity):

    @classmethod
    def get_rules(cls):
        return {
            'login': [
                FieldsValidator.VALIDATE_REQUIRED,
                FieldsValidator.VALIDATE_TYPE_STRING,
                validate_unique(cls)
            ],
            'password': [
                FieldsValidator.VALIDATE_REQUIRED,
                FieldsValidator.VALIDATE_TYPE_STRING,
            ]
        }

    def set_password(self, password):
        self.validator.fields['password'] = hash_password(password)

    @classmethod
    def authenticate(cls, login, password):
        user = cls.find_one({'login': login})
        if user and verify_password(password=password, stored_hash=user.password):
            return user

        return None
