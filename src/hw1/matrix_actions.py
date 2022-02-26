from typing import Iterable

from src.hw1.vector_actions import vector_sum, multiply as vector_multiply


def transpose(matrix: Iterable[Iterable[int]]) -> list[list[int]]:
    return [list(row) for row in zip(*matrix)]


def matrix_sum(*matrices: Iterable[Iterable[int]]) -> list[list[int]]:
    return [vector_sum(*rows) for rows in zip(*matrices)]


def multiply(matrix1: Iterable[Iterable[int]], matrix2: Iterable[Iterable[int]]) -> list[list[int]]:
    transposed_matrix2 = transpose(matrix2)
    return [[vector_multiply(row1, row2) for row2 in transposed_matrix2] for row1 in matrix1]
