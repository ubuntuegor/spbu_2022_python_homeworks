from multiprocessing import Process, Array
from array import array
from collections.abc import MutableSequence


def _swap_el(arr: MutableSequence, i: int, j: int):
    tmp = arr[i]
    arr[i] = arr[j]
    arr[j] = tmp


def _partition(arr: MutableSequence, start: int, end: int) -> int:
    pivot = arr[end - 1]
    j = start - 1

    for i in range(start, end - 1):
        if arr[i] < pivot:
            j += 1
            _swap_el(arr, i, j)

    j += 1
    _swap_el(arr, j, end - 1)
    return j


def _quick_sort_rec(arr: MutableSequence, start: int, end: int, depth: int):
    if end - start <= 1:
        return

    pivot_i = _partition(arr, start, end)

    if depth < 3:
        p = Process(target=_quick_sort_rec, args=(arr, start, pivot_i, depth + 1))
        p.start()
        _quick_sort_rec(arr, pivot_i + 1, end, depth + 1)
        p.join()
    else:
        _quick_sort_rec(arr, start, pivot_i, depth + 1)
        _quick_sort_rec(arr, pivot_i + 1, end, depth + 1)


def quick_sort(arr: array) -> array:
    shared_arr = Array(arr.typecode, arr, lock=False)
    _quick_sort_rec(shared_arr, 0, len(arr), 0)
    return array(arr.typecode, shared_arr)
