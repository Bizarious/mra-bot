from typing import Callable


def command(alias: str = None):
    def decorator(func: Callable):
        if alias is None:
            return Command(func, func.__name__)
        return Command(func, alias)
    return decorator


class Command:

    def __init__(self, func: Callable, name: str):
        self.__func = func
        self.__name = name

    def __call__(self, *args, **kwargs):
        return self.__func(*args, **kwargs)

    @property
    def name(self):
        return self.__name
