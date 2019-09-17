from reminder.security.authorization.user import User
from reminder.security.authorization import authenticate
from reminder.security.authorization.password import set_password
from reminder.web.rest.handlers import ValidationHandler, FieldsValidator


class SignUpHandler(ValidationHandler):

    @property
    def rules(self) -> dict:
        return {
            'login': [
                FieldsValidator.VALIDATE_REQUIRED,
                FieldsValidator.VALIDATE_TYPE_STRING,
            ],
            'password': [
                FieldsValidator.VALIDATE_REQUIRED,
                FieldsValidator.VALIDATE_TYPE_STRING,
            ]
        }

    async def handle(self, request):
        user = User(**self.validator.fields)
        set_password(user, self.validator.fields.get('password'))
        user.save()

        return self.send_json(user.to_dict(exclude=('password', )), status=201)


class SignInHandler(ValidationHandler):

    @property
    def rules(self) -> dict:
        return {
            'login': [
                FieldsValidator.VALIDATE_REQUIRED,
                FieldsValidator.VALIDATE_TYPE_STRING,
            ],
            'password': [
                FieldsValidator.VALIDATE_REQUIRED,
                FieldsValidator.VALIDATE_TYPE_STRING,
            ]
        }

    async def handle(self, request):
        user = authenticate(
            self.validator.fields.get('login'),
            self.validator.fields.get('password'))
        if not user:
            return self.send_error_json('Invalid credentials', status=401)

        return self.send_success_json('authenticated')
