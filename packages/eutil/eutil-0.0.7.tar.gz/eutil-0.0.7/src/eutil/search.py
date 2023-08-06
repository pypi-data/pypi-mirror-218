from typing import Iterable, Callable, TypeVar, NoReturn

T = TypeVar('T')


class Search:

    @staticmethod
    def linear(iterable: Iterable[T], predicate: Callable[[T], bool]) -> T:
        for x in iterable:
            if predicate(x):
                return x
        return None

    @staticmethod
    def binary() -> NoReturn: raise NotImplemented()

    @staticmethod
    def jump() -> NoReturn: raise NotImplemented()

    @staticmethod
    def interpolation() -> NoReturn: raise NotImplemented()

    @staticmethod
    def exponential() -> NoReturn: raise NotImplemented()

