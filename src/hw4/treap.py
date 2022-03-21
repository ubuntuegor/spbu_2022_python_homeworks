from operator import attrgetter
from random import randint
import sys


class _TreapNode:
    def __init__(self, key, value, priority):
        self.key = key
        self.value = value
        self.priority = priority
        self.left = None
        self.right = None

    def __iter__(self):
        if self.left != None:
            for node in self.left:
                yield node
        yield self
        if self.right != None:
            for node in self.right:
                yield node

    def find_child(self, key) -> "_TreapNode | None":
        if key == self.key:
            return self
        if key > self.key:
            if self.right == None:
                return None
            return self.right.find_child(key)
        else:
            if self.left == None:
                return None
            return self.left.find_child(key)

    @staticmethod
    def split(node: "_TreapNode | None", key) -> tuple["_TreapNode | None", "_TreapNode | None"]:
        if node == None:
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
    def merge(a: "_TreapNode | None", b: "_TreapNode | None") -> "_TreapNode | None":
        if a == None:
            return b
        if b == None:
            return a

        if a.priority > b.priority:
            a.right = _TreapNode.merge(a.right, b)
            return a
        else:
            b.left = _TreapNode.merge(a, b.left)
            return b


class _TreapTree:
    def __init__(self, *nodes: _TreapNode):
        queue = sorted(nodes, key=attrgetter("key"))

        while len(queue) > 1:
            new_queue = []
            if len(queue) % 2 != 0:
                queue.append(None)
            for pair in zip(queue[::2], queue[1::2]):
                new_queue.append(_TreapNode.merge(*pair))
            queue = new_queue

        self._root = queue[0] if len(queue) > 0 else None

    def __iter__(self):
        if self._root == None:
            return iter(())
        return iter(self._root)

    def clear(self):
        self._root = None

    def find_node(self, key) -> _TreapNode | None:
        if self._root == None:
            return None
        return self._root.find_child(key)

    def insert(self, node: _TreapNode):
        if self._root == None:
            self._root = node
            return
        parts = _TreapNode.split(self._root, node.key)
        self._root = _TreapNode.merge(_TreapNode.merge(parts[0], node), parts[1])

    def remove(self, key):
        if self._root == None:
            return
        parts = _TreapNode.split(self._root, key)
        self._root = _TreapNode.merge(*parts)


def _random_int():
    return randint(0, sys.maxsize)


class Treap:
    """
    Stores key-value pairs in a treap with randomized priority.

    Note: although any comparable values can serve as keys, you are advised
    to use integer values as they are the fastest to compare.
    """

    def __init__(self, dict: dict | None = None, /):
        "Create a treap and fill it with values from the optional `dict` dictionary."
        self._size = 0
        if dict != None:
            self._size = len(dict)
            nodes = (_TreapNode(key, value, _random_int()) for key, value in dict.items())
            self._tree = _TreapTree(*nodes)
        else:
            self._tree = _TreapTree()

    def clear(self):
        self._size = 0
        self._tree.clear()

    def get(self, key):
        node = self._tree.find_node(key)
        if node == None:
            return None
        return node.value

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

    def __contains__(self, key):
        node = self._tree.find_node(key)
        return node != None

    def __getitem__(self, key):
        node = self._tree.find_node(key)
        if node == None:
            raise KeyError(repr(key))
        return node.value

    def __setitem__(self, key, value):
        node = self._tree.find_node(key)
        if node == None:
            self._size += 1
            self._tree.insert(_TreapNode(key, value, _random_int()))
        else:
            node.value = value

    def __delitem__(self, key):
        node = self._tree.find_node(key)
        if node == None:
            raise KeyError(repr(key))
        self._size -= 1
        self._tree.remove(key)
