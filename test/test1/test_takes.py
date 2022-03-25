import pytest
from src.test1.takes import takes


@takes(int, str, somethingelse=bool)
def foo(num, string, *, somethingelse=False):
    pass


def test_takes():
    foo(1, "e")
    foo(1, "e", somethingelse=True)

    with pytest.raises(TypeError):
        foo("a", "e")
