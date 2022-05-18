from contextlib import contextmanager
from threading import Lock


class AtomicDict:
    "A dictionary which can be safely accessed from different threads"

    def __init__(self):
        self._data = {}
        self._lock = Lock()

    @contextmanager
    def acquire(self):
        "Context manager that sets the lock and provides the dictionary"
        self._lock.acquire()
        yield self._data
        self._lock.release()
