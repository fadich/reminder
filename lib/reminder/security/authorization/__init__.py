from .user import User
from .password import verify_password


def authenticate(login: str, password: str):
    _user = User.find_one({'login': login})
    if _user and verify_password(password=password, stored_hash=_user.password):
        return _user

    return None
