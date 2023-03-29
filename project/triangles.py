import pygraphblas as gb
from math import ceil
from project import is_NxN_bool_matrix
from typing import List, Tuple

__all__ = [
    "count_triangles_per_vertex",
    "count_triangles_cohen",
    "count_triangles_sandia",
]


def count_triangles_per_vertex(graph: gb.Matrix) -> List[int]:
    """For each vertex counts the number of triangles it correspond with.

    Args:
        graph (gb.Matrix): NxN symmetric bool matrix of the graph.

    Raises:
        ValueError: error if graph matrix is not NxN bool matrix.
        (don't check if graph is symmetric)

    Returns:
        List[int]: list of N numbers.
        For each vertex count of triangles it correspond with.
    """

    is_NxN_bool_matrix(graph)

    triangles = graph.mxm(graph, semiring=gb.INT64.PLUS_TIMES, mask=graph.S)
    triangles = triangles.reduce_vector()
    return [ceil(triangles.get(i, default=0) / 2) for i in range(triangles.size)]


def count_triangles_cohen(graph: gb.Matrix) -> int:
    """Counts the number of unique triangles in a graph using Cohen's algorithm.

    Args:
        graph (gb.Matrix): NxN symmetric bool matrix of the graph.

    Raises:
        ValueError: error if graph matrix is not NxN bool matrix.
        (don't check if graph is symmetric)

    Returns:
        int: number of unique triangles in a graph.
    """

    is_NxN_bool_matrix(graph)

    counts = graph.tril().mxm(graph.triu(), semiring=gb.INT64.PLUS_TIMES, mask=graph)
    return ceil(counts.reduce_int() / 2)


def count_triangles_sandia(graph: gb.Matrix) -> int:
    """Counts the number of unique triangles in a graph using Sandia's algorithm.

    Args:
        graph (gb.Matrix): NxN symmetric bool matrix of the graph.

    Raises:
        ValueError: error if graph matrix is not NxN bool matrix.
        (don't check if graph is symmetric)

    Returns:
        int: number of unique triangles in a graph.
    """

    is_NxN_bool_matrix(graph)

    tril = graph.tril()
    counts = tril.mxm(tril, semiring=gb.INT64.PLUS_TIMES, mask=tril)
    return counts.reduce_int()
