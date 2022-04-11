import sys
from abc import ABCMeta, abstractmethod
from itertools import zip_longest
from operator import attrgetter
from random import randint
from typing import Any, Generic, Optional, TypeVar, cast


class Comparable(metaclass=ABCMeta):
    @abstractmethod
    def __lt__(self, other: "K") -> bool:
        pass


K = TypeVar("K", bound=Comparable)


class _TreapNode(Generic[K]):
    def __init__(self, key: K, value, priority: int):
        self.key = key
        self.value = value
        self.priority = priority
        self.left: "Optional[_TreapNode[K]]" = None
        self.right: "Optional[_TreapNode[K]]" = None

    def __iter__(self):
        if self.left is not None:
            for node in self.left:
                yield node
        yield self
        if self.right is not None:
            for node in self.right:
                yield node

    def find_child(self, key: K) -> "Optional[_TreapNode[K]]":
        if key == self.key:
            return self
        if key > self.key:
            if self.right is None:
                return None
            return self.right.find_child(key)
        else:
            if self.left is None:
                return None
            return self.left.find_child(key)

    def split(self, key: K) -> tuple["Optional[_TreapNode[K]]", "Optional[_TreapNode[K]]", "Optional[_TreapNode[K]]"]:
        """Splits the tree and returns 3 subtrees: less than `key`, greater than `key`, equal to `key`"""
        if key > self.key:
            parts = self.right.split(key) if self.right is not None else (None, None, None)
            self.right = parts[0]
            return (self, parts[1], parts[2])
        elif key < self.key:
            parts = self.left.split(key) if self.left is not None else (None, None, None)
            self.left = parts[1]
            return (parts[0], self, parts[2])
        else:
            left = self.left
            right = self.right
            self.left = self.right = None
            return (left, right, self)

    def merge_with(self, other: "Optional[_TreapNode[K]]") -> "_TreapNode[K]":
        """Makes a new tree out of `self` and `other`. Each key in `self` must be smaller than any key in `other`"""
        if other is None:
            return self

        if self.priority > other.priority:
            self.right = self.right.merge_with(other) if self.right is not None else other
            return self
        else:
            other.left = self.merge_with(other.left)
            return other


def _random_int():
    return randint(0, sys.maxsize)


class Treap(Generic[K]):
    """
    Stores key-value pairs in a treap with randomized priority.

    Note: although any comparable values can serve as keys, you are advised
    to use integer values as they are the fastest to compare.
    """

    def __init__(self, from_dict: Optional[dict[K, Any]] = None, /):
        """Create a treap and fill it with values from the optional `dict` dictionary."""
        self._size: int = 0
        self._root: Optional[_TreapNode] = None

        if from_dict is not None and len(from_dict) > 0:
            self._size = len(from_dict)
            nodes = [_TreapNode(key, value, _random_int()) for key, value in from_dict.items()]
            queue: list[_TreapNode[K]] = sorted(nodes, key=attrgetter("key"))

            while len(queue) > 1:
                new_queue: list[_TreapNode[K]] = []
                for left, right in zip_longest(queue[::2], queue[1::2]):
                    if left is not None:
                        new_queue.append(left.merge_with(right))
                queue = new_queue

            self._root = queue[0]

    def _find_node(self, key: K) -> Optional[_TreapNode]:
        return self._root and self._root.find_child(key)

    def clear(self):
        self._size = 0
        self._root = None

    def get(self, key: K):
        node = self._find_node(key)
        return node.value if (node is not None) else None

    def __iter__(self):
        if self._root is not None:
            for node in self._root:
                yield node.key

    def __repr__(self):
        pairs = []
        for key in self:
            pairs.append(repr(key) + ": " + repr(self[key]))
        return self.__class__.__name__ + "({" + ", ".join(pairs) + "})"

    def __len__(self):
        return self._size

    def __contains__(self, key: K):
        node = self._find_node(key)
        return node is not None

    def __getitem__(self, key: K):
        node = self._find_node(key)
        if node is None:
            raise KeyError(repr(key))
        return node.value

    def __setitem__(self, key: K, value):
        node = self._find_node(key)
        if node is not None:
            node.value = value
        else:
            self._size += 1
            node = _TreapNode(key, value, _random_int())
            if self._root is not None:
                left, right, _ = self._root.split(node.key)
                if left is not None:
                    self._root = left.merge_with(node).merge_with(right)
                else:
                    self._root = node.merge_with(right)
            else:
                self._root = node

    def __delitem__(self, key: K):
        node = self._find_node(key)
        if node is not None:
            self._size -= 1
            left, right, _ = cast(_TreapNode[K], self._root).split(key)
            self._root = left.merge_with(right) if left is not None else right
        else:
            raise KeyError(repr(key))
