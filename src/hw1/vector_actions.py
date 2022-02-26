from math import sqrt, acos
from typing import Iterable


def vector_sum(*vectors: Iterable[int]) -> list[int]:
    return [sum(n) for n in zip(*vectors)]


def multiply(vec1: Iterable[int], vec2: Iterable[int]) -> int:
    return sum(i[0] * i[1] for i in zip(vec1, vec2))


def length(vec: Iterable[int]) -> float:
    return sqrt(sum([i**2 for i in vec]))


def angle(vec1: Iterable[int], vec2: Iterable[int]) -> float:
    return acos(multiply(vec1, vec2) / (length(vec1) * length(vec2)))
