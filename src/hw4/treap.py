from operator import attrgetter
from random import randint
import sys
from typing import Any, Generic, Optional, TypeVar


class _TreapNode:
    key: Any
    value: Any
    priority: int
    left: "Optional[_TreapNode]"
    right: "Optional[_TreapNode]"

    def __init__(self, key, value, priority):
        self.key = key
        self.value = value
        self.priority = priority
        self.left = None
        self.right = None

    def __iter__(self):
        if self.left is not None:
            for node in self.left:
                yield node
        yield self
        if self.right is not None:
            for node in self.right:
                yield node

    def find_child(self, key) -> "Optional[_TreapNode]":
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

    @staticmethod
    def split(node: "Optional[_TreapNode]", key) -> tuple["Optional[_TreapNode]", "Optional[_TreapNode]"]:
        if node is None:
            return (None, None)
        if key > node.key:
            parts = _TreapNode.split(node.right, key)
            node.right = parts[0]
            return (node, parts[1])
        elif key < node.key:
            parts = _TreapNode.split(node.left, key)
            node.left = parts[1]
            return (parts[0], node)
        else:
            return (node.left, node.right)

    @staticmethod
    def merge(a: "Optional[_TreapNode]", b: "Optional[_TreapNode]") -> "Optional[_TreapNode]":
        if a is None:
            return b
        if b is None:
            return a

        if a.priority > b.priority:
            a.right = _TreapNode.merge(a.right, b)
            return a
        else:
            b.left = _TreapNode.merge(a, b.left)
            return b


class _TreapTree:
    _root: Optional[_TreapNode]

    def __init__(self, *nodes: _TreapNode):
        queue: list[_TreapNode | None] = sorted(nodes, key=attrgetter("key"))

        while len(queue) > 1:
            new_queue = []
            if len(queue) % 2 != 0:
                queue.append(None)
            for pair in zip(queue[::2], queue[1::2]):
                new_queue.append(_TreapNode.merge(*pair))
            queue = new_queue

        self._root = queue[0] if len(queue) > 0 else None

    def __iter__(self):
        if self._root is None:
            return iter(())
        return iter(self._root)

    def clear(self):
        self._root = None

    def find_node(self, key) -> Optional[_TreapNode]:
        if self._root is None:
            return None
        return self._root.find_child(key)

    def insert(self, node: _TreapNode):
        if self._root is not None:
            parts = _TreapNode.split(self._root, node.key)
            self._root = _TreapNode.merge(_TreapNode.merge(parts[0], node), parts[1])
        else:
            self._root = node

    def remove(self, key):
        if self._root is None:
            return
        parts = _TreapNode.split(self._root, key)
        self._root = _TreapNode.merge(*parts)


def _random_int():
    return randint(0, sys.maxsize)


K = TypeVar("K")


class Treap(Generic[K]):
    """
    Stores key-value pairs in a treap with randomized priority.

    Note: although any comparable values can serve as keys, you are advised
    to use integer values as they are the fastest to compare.
    """

    _size: int
    _tree: _TreapTree

    def __init__(self, from_dict: dict | None = None, /):
        "Create a treap and fill it with values from the optional `dict` dictionary."
        self._size = 0
        if from_dict is not None:
            self._size = len(from_dict)
            nodes = (_TreapNode(key, value, _random_int()) for key, value in from_dict.items())
            self._tree = _TreapTree(*nodes)
        else:
            self._tree = _TreapTree()

    def clear(self):
        self._size = 0
        self._tree.clear()

    def get(self, key: K):
        node = self._tree.find_node(key)
        return node.value if (node is not None) else None

    def __iter__(self):
        for node in self._tree:
            yield node.key

    def __repr__(self):
        pairs = []
        for key in self:
            pairs.append(repr(key) + ": " + repr(self[key]))
        return self.__class__.__name__ + "({" + ", ".join(pairs) + "})"

    def __len__(self):
        return self._size

    def __contains__(self, key: K):
        node = self._tree.find_node(key)
        return node is not None

    def __getitem__(self, key: K):
        node = self._tree.find_node(key)
        if node is None:
            raise KeyError(repr(key))
        return node.value

    def __setitem__(self, key: K, value):
        node = self._tree.find_node(key)
        if node is not None:
            node.value = value
        else:
            self._size += 1
            self._tree.insert(_TreapNode(key, value, _random_int()))

    def __delitem__(self, key: K):
        node = self._tree.find_node(key)
        if node is not None:
            self._size -= 1
            self._tree.remove(key)
        else:
            raise KeyError(repr(key))
