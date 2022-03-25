from functools import wraps
import inspect
import time
from typing import Callable, Generator


def spy(f: Callable) -> Callable:
    @wraps(f)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            argspec = inspect.getfullargspec(f)
            positional_names = argspec.args
            all_args = dict(zip(positional_names, args))
            if argspec.varargs is not None and len(args) > len(positional_names):
                all_args[argspec.varargs] = args[len(positional_names) :]
            all_args.update(kwargs)
        except ValueError:
            all_args = dict(enumerate(args))
            all_args.update(kwargs)
        wrapper._spy_data.append((start_time, all_args))
        return f(*args, **kwargs)

    wrapper._spy_data = []  # type: ignore[attr-defined]
    return wrapper


def usage_statistics(function: Callable) -> Generator[tuple[float, dict], None, None]:
    if hasattr(function, "_spy_data"):
        for pair in function._spy_data:  # type: ignore[attr-defined]
            yield pair
