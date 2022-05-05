from random import shuffle
from array import array
import pytest
from src.test2.quicksort import quick_sort


@pytest.mark.parametrize("size", [10, 1000, 10000])
def test_quicksort(size: int):
    a = array("i", range(size))
    shuffle(a)
    b = quick_sort(a)
    c = array("i", sorted(a))
    assert c == b
