from collections.abc import Sequence

from src.hw1.vector_actions import vector_sum, multiply as vector_multiply

Matrix = Sequence[Sequence[int]]


def transpose(matrix: Matrix) -> Matrix:
    return [list(row) for row in zip(*matrix)]


def matrix_sum(*matrices: Matrix) -> Matrix:
    return [vector_sum(*rows) for rows in zip(*matrices)]


def multiply(matrix1: Matrix, matrix2: Matrix) -> Matrix:
    transposed_matrix2 = transpose(matrix2)
    return [[vector_multiply(row1, row2) for row2 in transposed_matrix2] for row1 in matrix1]
