from typing import Callable
from logging import getLogger

from reminder.exceptions import DeprecatedError


logger = getLogger(__name__)


class BaseDecorator(object):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class ComputedPropertyMeta(type):
    pass


class property(BaseDecorator, metaclass=ComputedPropertyMeta):

    def __call__(self, func: Callable):
        return func(*self.args, **self.kwargs)


class cashed_property(property):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.func: Callable = None

    def __call__(self, func: Callable):
        if not self.func:
            self.func = func

        return super().__call__(self.func)


class deprecated(BaseDecorator):

    def __init__(self, raise_error=True, *args, **kwargs):
        self.raise_error = raise_error
        super().__init__(*args, **kwargs)

    def __call__(self, func: Callable):
        error_msg = f'Calling of deprecated function {func.__name__}'
        if not self.raise_error:
            logger.warning(error_msg)
            return func

        raise DeprecatedError(error_msg)


if __name__ == '__main__':

    @property(word='There!')
    def hello(word: str = 'World'):
        return f'Hello {word}'

    print(hello)

    @cashed_property()
    def get_time():
        import time
        return time.time()

    print(get_time)
    print(get_time)
