import math
from typing import List, Tuple
from project.utils import is_NxN_matrix, start_vertex_out_of_range_error

import pygraphblas as gb

__all__ = ["sssp", "mssp", "apsp"]


def sssp(graph: gb.Matrix, start: int) -> List[int]:
    """Finds Single-Source Shortest Paths distances using an Bellman-Ford algorithm.

    Args:
        graph (gb.Matrix):  NxN matrix of the graph.
        start (int):        path start index (from 0 to N - 1).

    Raises:
        ValueError: error if graph matrix is not NxN matrix.
        ValueError: error start vertex is out of range.

    Returns:
        List[int]: distance to current vertex from start.
        None if vertex unreachable from start vertex.
    """

    return mssp(graph, [start])[0][1]


def mssp(graph: gb.Matrix, start_vector: List[int]) -> List[Tuple[int, List[int]]]:
    """Finds Multiple-Source Shortest Paths lengths using an Bellman-Ford algorithm.

    Args:
        graph (gb.Matrix):          NxN matrix of the graph.
        start_vector (List[int]):   path start indexes (from 0 to N - 1).

    Raises:
        ValueError: error if graph matrix is not NxN matrix.
        ValueError: error start vertex is out of range.

    Returns:
        List[Tuple[int, List[int]]]: (start vertex, list of distance to current vertex from start)
        None if vertex unreachable from start vertex.
    """

    is_NxN_matrix(graph)

    n = graph.ncols
    m = len(start_vector)
    gtype = graph.type

    front = gb.Matrix.sparse(gtype, nrows=m, ncols=n)

    for row, start in enumerate(start_vector):
        if start < 0 or start >= n:
            raise start_vertex_out_of_range_error(start)
        front[row, start] = 0

    for _ in range(n):
        front.mxm(graph, semiring=gtype.MIN_PLUS, out=front, accum=gtype.MIN)

    return [
        (start, [front.get(row, col, default=None) for col in range(n)])
        for row, start in enumerate(start_vector)
    ]


def apsp(graph: gb.Matrix) -> List[Tuple[int, List[int]]]:
    """Finds All-Pairs Shortest Paths distances using an Floyd-Warshall algorithm.

    Args:
        graph (gb.Matrix): NxN matrix of the graph.

    Raises:
        ValueError: error if graph matrix is not NxN matrix.

    Returns:
        List[Tuple[int, List[int]]]: (start vertex, list of distance to current vertex from start)
        None if vertex unreachable from start vertex.
    """

    is_NxN_matrix(graph)

    n = graph.ncols
    gtype = graph.type

    front = graph.dup()

    for k in range(n):
        step = front.extract_matrix(col_index=k).mxm(
            front.extract_matrix(row_index=k),
            semiring=gtype.MIN_PLUS,
        )
        front.eadd(step, add_op=gtype.MIN, out=front)
        front[k, k] = 0

    return [
        (row, [front.get(row, col, default=None) for col in range(n)])
        for row in range(n)
    ]
