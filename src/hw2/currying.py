from typing import Callable, Tuple


def curry_explicit(f: Callable, n: int) -> Callable:
    "Applies currying to f with a fixed number (n) of positional arguments"

    if n < 0:
        raise ValueError("Function cannot have a negative number of arguments")

    def closure(n: int, args: Tuple) -> Callable:
        if n == 0:
            return lambda: f(*args)
        if n == 1:
            return lambda x: f(*args, x)
        return lambda x: closure(n - 1, args + (x,))

    return closure(n, ())
