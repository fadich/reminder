from typing import Callable


class ComputedPropertyMeta(type):
    pass


class Property(metaclass=ComputedPropertyMeta):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, func: Callable):
        return func(*self.args, **self.kwargs)


class CashedProperty(Property):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.func: Callable = None

    def __call__(self, func: Callable):
        if not self.func:
            self.func = func

        return super().__call__(self.func)


if __name__ == '__main__':

    @Property(word='There!')
    def hello(word: str = 'World'):
        return f'Hello {word}'

    print(hello)

    @CashedProperty()
    def get_time():
        import time
        return time.time()

    print(get_time)
    print(get_time)
