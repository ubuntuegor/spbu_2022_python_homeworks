from functools import wraps
from typing import Callable
from datetime import datetime


def safe_call(filename: str) -> Callable:
    def wrappee(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except BaseException as e:
                with open(filename, "a") as log:
                    now = datetime.now()
                    log.write(f"{now}: {repr(e)}\n")
                return None

        return wrapper

    return wrappee
