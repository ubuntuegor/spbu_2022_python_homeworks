from math import sqrt, acos
from collections.abc import Sequence

Vector = Sequence[int]


def vector_sum(*vectors: Vector) -> Vector:
    return [sum(n) for n in zip(*vectors)]


def multiply(vec1: Vector, vec2: Vector) -> int:
    return sum(i[0] * i[1] for i in zip(vec1, vec2))


def length(vec: Vector) -> float:
    return sqrt(sum([i**2 for i in vec]))


def angle(vec1: Vector, vec2: Vector) -> float:
    return acos(multiply(vec1, vec2) / (length(vec1) * length(vec2)))
