from typing import Iterable, Callable, TypeVar, NoReturn

T = TypeVar('T')


def linear_search(iterable: Iterable[T], predicate: Callable[[T], bool]) -> T:
    for x in iterable:
        if predicate(x):
            return x
    return None


def binary() -> NoReturn: raise NotImplemented()


def jump() -> NoReturn: raise NotImplemented()


def interpolation() -> NoReturn: raise NotImplemented()

def exponential() -> NoReturn: raise NotImplemented()


__all__ = ['linear_search']
