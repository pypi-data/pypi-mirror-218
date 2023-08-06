from typing import TypeVar, Optional, Type, Generic, get_origin
from abc import ABC, abstractmethod

from ..common import Node

T = TypeVar('T')





class BinaryTree:
    def __init__(self, root: Optional[BinaryNode] = None):
        self._root = root

    @property
    def root(self) -> Optional[BinaryNode]:
        return self._root

    @root.setter
    def root(self, node: Optional[BinaryNode]) -> None:
        if not isinstance(node, BinaryNode):
            raise TypeError()
        self._root = node


__all__ = ['BinaryTree']
