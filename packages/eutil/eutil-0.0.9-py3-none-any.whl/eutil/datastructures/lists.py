from typing import TypeVar, Optional, Type, Generic, get_origin, Any, NewType, Literal, Callable, Iterable
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from .common import Node

T = TypeVar('T')





class LinkedNode: ...


class LinkedList(Generic[T]): ...



#__all__ = ['LinkedList', 'LinkedNode']
