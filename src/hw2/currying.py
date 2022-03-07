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


def uncurry_explicit(f: Callable, n: int) -> Callable:
    "Uncurries the function f with n positional arguments"

    if n < 0:
        raise ValueError("Function cannot have a negative number of arguments")

    def uncurry(*args) -> Callable:
        if len(args) != n:
            raise ValueError(f"Uncurrying {n} arguments but {len(args)} were passed")

        result = f if n > 0 else f()
        for arg in args:
            result = result(arg)
        return result

    return uncurry
