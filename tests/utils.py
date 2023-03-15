import pygraphblas as gb
from typing import List, Tuple

__all__ = ["matrix_from_edges"]


def matrix_from_edges(size: int, edges: List[Tuple[int, int]]) -> gb.Matrix:
    """Generates gb.Matrix from list of edges

    Args:
        size (int): graph size
        edges (List[Tuple[int, int]]): list of graph edges

    Returns:
        gb.Matrix: graph
    """
    I = []
    J = []
    for i, j in edges:
        I.append(i)
        J.append(j)
    return gb.Matrix.from_lists(I, J, [True] * len(I), nrows=size, ncols=size)
