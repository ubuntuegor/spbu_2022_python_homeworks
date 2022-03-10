from contextlib import contextmanager
from threading import Lock


class AtomicDict:
    def __init__(self):
        self.__data__ = {}
        self.__lock__ = Lock()

    @contextmanager
    def acquire(self):
        self.__lock__.acquire()
        yield self.__data__
        self.__lock__.release()
