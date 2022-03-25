from functools import wraps
from typing import Callable


def takes(*types, **kwtypes):
    def decor(f: Callable):
        @wraps(f)
        def wrapper(*args, **kwargs):
            for arg_type, arg in zip(types, args):
                if not isinstance(arg, arg_type):
                    raise TypeError(f"Expected {arg_type}, got {type(arg)}")
            for key, value in kwargs.items():
                if key in kwtypes and not isinstance(value, kwtypes[key]):
                    raise TypeError(f"Expected {kwtypes[key]}, got {type(value)}")
            return f(*args, **kwargs)

        return wrapper

    return decor
