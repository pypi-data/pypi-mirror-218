from typing import Iterable, Callable, TypeVar, Any

T = TypeVar('T')


class Predicate:

    @staticmethod
    def match_property(attr_name: str, value: Any) -> Callable[[T], bool]:
        def predicate(obj: T) -> bool:
            if hasattr(obj, attr_name):
                raise ValueError()
            return getattr(obj, attr_name) == value

        return predicate


    @staticmethod
    def match(val: T) -> Callable[[T], bool]:
        def predicate(obj: T) -> bool:
            if not hasattr(obj, '__eq__'):
                raise ValueError()
            return obj == val

        return predicate
