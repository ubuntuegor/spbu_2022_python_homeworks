import pytest
from src.hw2.currying import curry_explicit, uncurry_explicit


def test_curry_explicit():
    fun = curry_explicit(lambda x, y, z: f"<{x},{y},{z}>", 3)
    assert fun(123)(456)(789) == "<123,456,789>"

    fun1 = fun("base")
    fun1_1 = fun1("option1")
    fun1_2 = fun1("option2")
    assert fun1_1("used") == "<base,option1,used>"
    assert fun1_2("used") == "<base,option2,used>"

    assert curry_explicit(lambda: "value", 0)() == "value"
    assert curry_explicit(lambda x: str(x), 1)(10) == "10"


def test_curry_explicit_freeze():
    fun = curry_explicit(lambda *args: "<{}>".format(", ".join(args)), 2)
    assert fun("ab")("cd") == "<ab, cd>"
    with pytest.raises(TypeError, match=".* is not callable"):
        fun("ab")("cd")("de")


def test_curry_explicit_fool():
    with pytest.raises(ValueError, match=".* negative number of arguments"):
        curry_explicit(lambda x: x, -1)


def test_uncurry_explicit():
    src = curry_explicit(lambda x, y, z: f"<{x},{y},{z}>", 3)
    fun = uncurry_explicit(src, 3)
    assert fun(123, 456, 789) == "<123,456,789>"

    src = curry_explicit(lambda: "value", 0)
    fun = uncurry_explicit(src, 0)
    assert fun() == "value"


def test_uncurry_explicit_fool():
    src = curry_explicit(lambda x, y, z: f"<{x},{y},{z}>", 3)
    with pytest.raises(ValueError, match=".* negative number of arguments"):
        uncurry_explicit(src, -1)

    fun = uncurry_explicit(src, 3)

    with pytest.raises(ValueError, match="Uncurrying 3 arguments but 2 were passed"):
        fun(1, 2)
