from itertools import chain
from typing import Union


def get_subclass[T](cls: Union[type[T], list[type[T]]]) -> list[type[T]]:
    if isinstance(cls, list):
        return list(chain(*[get_subclass(c) for c in cls]))
    elif subcls := cls.__subclasses__():
        return get_subclass(subcls) + [cls]
    return [cls]


__all__ = [
    'get_subclass',
]