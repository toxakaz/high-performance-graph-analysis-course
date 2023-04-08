import pygraphblas as gb
from typing import List, Tuple
from project.utils import is_NxN_bool_matrix, start_vertex_out_of_range_error


__all__ = ["bfs", "msbfs"]


def bfs(graph: gb.Matrix, start: int) -> List[int]:
    """BFS on a directed graph.

    Args:
        graph (gb.Matrix):  NxN bool matrix of the graph.
        start (int):        bfs start index (from 0 to N - 1).

    Raises:
        ValueError: error if graph matrix is not NxN bool matrix.
        ValueError: error start vertex is out of range.

    Returns:
        List[int]: a list, where for each vertex it is indicated at what step it is reachable.
        The starting vertex is reachable at the 0 step,
        if the vertex is not reachable, then the value of the corresponding cell is -1.
    """

    is_NxN_bool_matrix(graph)
    if start < 0 or start >= graph.nrows:
        raise start_vertex_out_of_range_error(start)

    steps = gb.Vector.sparse(gb.INT64, size=graph.nrows)
    front = gb.Vector.sparse(gb.BOOL, size=graph.nrows)

    steps[start] = 0
    front[start] = True
    step = 1

    while front.reduce():
        front.vxm(graph, out=front, mask=steps.S, desc=gb.descriptor.RC)
        steps.assign_scalar(step, mask=front)
        step += 1

    return [steps.get(i, default=-1) for i in range(steps.size)]


def msbfs(graph: gb.Matrix, start_vector: List[int]) -> List[Tuple[int, List[int]]]:
    """BFS on a directed graph from multiple source.

    Args:
        graph (gb.Matrix):          NxN bool matrix of the graph.
        start_vertex (List[int]):   bfs start indexes (from 0 to N - 1).

    Raises:
        ValueError: error if graph matrix is not NxN bool matrix.
        ValueError: error start vertex is out of range.

    Returns:
        List[Tuple[int, List[int]]]: a list of pairs (start, parents),
        where for each start vertex there is a list of parent vertices.
        If there are several possible parent vertices,
        the one with the lower index will be selected.
        Starting vertices will have -1 in these lists,
        and unreachable vertices will have -2.
    """

    is_NxN_bool_matrix(graph)

    n = graph.ncols
    m = len(start_vector)

    parents = gb.Matrix.sparse(gb.INT64, nrows=m, ncols=n)
    front = gb.Matrix.sparse(gb.INT64, nrows=m, ncols=n)

    for row, start in enumerate(start_vector):
        if start < 0 or start >= n:
            raise start_vertex_out_of_range_error(start)
        parents[row, start] = -1
        front[row, start] = start

    while front.nvals > 0:
        front.mxm(
            graph,
            out=front,
            semiring=gb.INT64.MIN_FIRST,
            mask=parents.S,
            desc=gb.descriptor.RC,
        )
        parents.assign(front, mask=front.S)
        front.apply(gb.INT64.POSITIONJ, out=front, mask=front.S)

    return [
        (start, [parents.get(row, col, default=-2) for col in range(n)])
        for row, start in enumerate(start_vector)
    ]
