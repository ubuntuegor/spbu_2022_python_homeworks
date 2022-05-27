from typing import Callable
from datetime import datetime


def logger(filename: str) -> Callable:
    def wrappee(f: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)
            with open(filename, "a") as log:
                datetime_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                log.write(f"{datetime_string} {f.__name__} {args} {kwargs} {result}\n")
            return result

        return wrapper

    return wrappee
