import math
from src.hw1.vector_actions import *


def test_sum_1():
    vec1 = [1, 2, 3]
    vec2 = [4, 5, 6]
    assert vector_sum(vec1, vec2) == [5, 7, 9]


def test_sum_2():
    vec1 = [1, 1]
    vec2 = [2, 2]
    vec3 = [3, 4]
    assert vector_sum(vec1, vec2, vec3) == [6, 7]


def test_multiply_1():
    vec1 = [1, 0]
    vec2 = [0, 1]
    assert multiply(vec1, vec2) == 0


def test_multiply_2():
    vec1 = [1, 8, 3]
    vec2 = [6, 8, 9]
    assert multiply(vec1, vec2) == 6 + (8 * 8) + (3 * 9)


def test_empty_length():
    vec = [0, 0, 0]
    assert length(vec) == 0.0


def test_length():
    vec = [3, 4]
    assert length(vec) == 5.0


def test_angle():
    vec1 = [0, 1]
    vec2 = [1, 0]
    assert angle(vec1, vec2) == math.pi / 2
