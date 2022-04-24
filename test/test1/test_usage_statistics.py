import time

import pytest
from src.test1.usage_statistics import spy, usage_statistics


def fail(num):
    print(num)


@spy
def foo(num):
    print(num)


@spy
def bar(arg1, arg2, arg3=3, *posargs, **kwargs):
    pass


def test_usage_statistics_foo():
    start_time = time.time()
    foo(1)
    foo(2)

    stats = list(usage_statistics(foo))
    timestamps = [pair[0] for pair in stats]
    passed_args = [pair[1] for pair in stats]
    assert all([start_time <= ts <= time.time() for ts in timestamps])
    assert len(passed_args[0]) == 1
    assert passed_args == [{"num": 1}, {"num": 2}]


def test_usage_statistics_bar():
    bar(1, 2, arg3=3)
    bar(1, 2, 3, 4, 5, test=6)

    stats = list(usage_statistics(bar))
    passed_args = [pair[1] for pair in stats]
    assert passed_args[0] == {"arg1": 1, "arg2": 2, "arg3": 3}
    assert passed_args[1] == {"arg1": 1, "arg2": 2, "arg3": 3, "posargs": (4, 5), "test": 6}


def test_usage_statistics_fail():
    with pytest.raises(TypeError):
        list(usage_statistics(fail))
