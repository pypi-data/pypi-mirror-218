from __future__ import annotations

from typing import TypeVar, Optional, Type, Generic, get_origin, Any, NewType, Literal, Callable, Iterable
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

T = TypeVar('T')


class Array(Generic[T]):
    def __init__(self, size: int, fill: Optional[T] = None, default: Optional[T] = None):
        self._size = size
        self._default = default
        self._data = [fill for _ in range(size)]
        self._empty: 0 | 1 | 2 = 1 if fill is None else 0

    def __repr__(self) -> str:
        return '[' + ', '.join([str(x) for x in self._data]) + ']'

    def __getitem__(self, index: int) -> Optional[T]:
        return self.get(index)

    def __setitem__(self, index: int, value: Optional[T]):
        return self.set(index, value)

    def __iter__(self):
        return iter(self._data)

    def get(self, index: int) -> Optional[T]:
        if not self._valid_index(index):
            raise IndexError()
        return self._data[index]

    def set(self, index: int, value: Optional[T]) -> bool:
        if not self._valid_index(index):
            raise IndexError()
        curr = self._data[index]
        if curr == value:
            return False
        self._data[index] = value
        return True

    def search(self, search_method: Callable[[Iterable, Callable[[Optional[T]], bool]], Optional[T]],
               predicate: Callable[[Optional[T]], bool]) -> Optional[T]:
        return search_method(self._data, predicate)

    def _is_empty(self) -> int:
        for item in self._data:
            item: Optional[T]
            if item != self._default:
                return 0
        return 1

    def _valid_index(self, index: int):
        if not isinstance(index, int):
            return False
        return self.size >= index >= 0

    @property
    def size(self):
        return self._size

    @property
    def length(self):
        return self._size

    @property
    def is_empty(self) -> bool:
        if self._empty == 2:
            self._empty = self._is_empty()
        return bool(self._empty)

    @classmethod
    def from_iterable(cls, iterable: Iterable[T], default: Optional[T] = None) -> Array:
        length = len([x for x in iterable])
        new = Array(size=length, default=default)
        for i in range(length):
            new[i] = iterable[i]
        return new


class Node(ABC, Generic[T]):

    def __init__(self, data, **kwargs):
        self._data: Optional[T] = data
        self._links: Array[Node[T]] = self._init_links(kwargs)

    def _init_links(self, kwargs: dict[str, Node[T]]) -> Array[Node[T]]:
        array = Array.from_iterable(list(kwargs.values()))
        for i, key in enumerate(kwargs):
            setattr(self, f'_{key}', lambda: array.get(i))
        return array

    def change_links(self, new_links: dict[str, Node[T]]) -> None:
        self._links = self._init_links(new_links)

    def __repr__(self):
        return f'Node({str(self._data)})'

    def __eq__(self, other: Node):
        if not isinstance(other, Node):
            return False
        if not get_origin(other.data) == get_origin(self._data):
            return False
        return other.data == self._data

    @property
    def data(self) -> Optional[T]:
        return self._data

    @data.setter
    def data(self, data: Optional[T]):
        self._data = data

    @property
    def links(self):
        return self._links


@dataclass(order=True)
class SinglyLinkedNode(Node):
    __data: Optional[T] = field(compare=False)
    __next: Optional[Node] = field(compare=False)

    def __post_init__(self):
        super().__init__(self.__data, next=self.__next)

    @property
    def next(self):
        next_node: Callable[[], Node[Optional[T]]] = getattr(self, '_next')
        return next_node()

    @next.setter
    def next(self, node: Node[T]):
        links = {'next': node}
        self.change_links(links)


@dataclass(order=True)
class DoublyLinkedNode(Node):
    __data: Optional[T] = field(compare=False)
    __left: Optional[Node] = field(compare=False)
    __right: Optional[Node] = field(compare=False)
    _names: tuple[str, str] = field(compare=False)

    def __post_init__(self):
        super().__init__(self.__data, left=self.__left, right=self.__right)

    def __setattr__(self, key, value):
        print('called', key, '=', value)
        if key != '_names':
            if len(vars(self)) > 7:
                if key not in vars(self) and key not in self._names:
                    raise KeyError(key)

            if hasattr(self, '_names'):
                if key in self._names:
                    if key == self._names[0]:
                        self.links[0] = value
                    elif key == self._names[1]:
                        self.links[1] = value
        super().__setattr__(key, value)


class LinkedList(Generic[T]):
    def __init__(self, root: Optional[SinglyLinkedNode[T]] = None):
        self._root = root

    def add(self, data: T):
        new_node = SinglyLinkedNode(data, None)




__all__ = [
    # DS
    'LinkedList',
    'Array'
    # Nodes
    'Node',
    'SinglyLinkedNode',
    'DoublyLinkedNode'
]


