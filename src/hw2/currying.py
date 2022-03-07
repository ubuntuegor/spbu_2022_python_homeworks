from typing import Callable, Tuple


def curry_explicit(f: Callable, n: int) -> Callable:
    "Applies currying to f with a fixed number (n) of positional arguments"

    if n < 0:
        raise ValueError("Function cannot have a negative number of arguments")

    def closure(f: Callable, n: int, args: Tuple) -> Callable:
        if n == 0:
            return lambda: f(*args)
        if n == 1:
            return lambda x: f(*args, x)
        return lambda x: closure(f, n - 1, args + (x,))

    return closure(f, n, ())


f2 = curry_explicit((lambda x, y, z: f"<{x},{y},{z}>"), 3)
f1 = curry_explicit((lambda: "Hello!"), 0)
ff = f2(123)(456)
fd = f2(123)(987)
print(ff(4444))
print(fd(7686))
print(f1())
curry_explicit(print, 2)(1)(2)
