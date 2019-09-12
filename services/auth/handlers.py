from reminder.security.user import User
from reminder.web.rest.handlers import ValidationHandler, FieldsValidator


class SignUpHandler(ValidationHandler):

    @property
    def rules(self) -> dict:
        return User.get_rules()

    async def handle(self, request):
        user = User(**self.validator.fields)
        user.set_password(user.password)
        user.save()

        return self.send_json({
            'login': user.login,
            '_id': str(user.object_id),
        }, status=201)


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
        user = User.authenticate(
            self.validator.fields.get('login'),
            self.validator.fields.get('password'))
        if not user:
            return self.send_error_json('Invalid credentials', status=401)

        return self.send_success_json('authenticated')
