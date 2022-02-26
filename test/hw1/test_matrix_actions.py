from src.hw1.matrix_actions import *


def test_transpose():
    matrix = [[1, 2], [3, 4], [5, 6]]
    transposed_matrix = [[1, 3, 5], [2, 4, 6]]
    assert transpose(matrix) == transposed_matrix


def test_matrix_sum():
    matrix1 = [[1, 3], [2, 9]]
    matrix2 = [[0, 1], [-1, 1]]
    assert matrix_sum(matrix1, matrix2) == [[1, 4], [1, 10]]


def test_multiply():
    matrix1 = [[10, 2], [3, 9], [6, 7]]
    matrix2 = [[9, 9], [9, 4]]
    assert multiply(matrix1, matrix2) == [[108, 98], [108, 63], [117, 82]]
