import pygraphblas as gb
import networkx as nx
from typing import List, Tuple


__all__ = [
    "matrix_from_edges",
    "read_graph",
    "is_NxN_bool_matrix",
    "start_vertex_out_of_range_error",
]


def matrix_from_edges(
    size: int, edges: List[Tuple[int, int]], is_directed: bool = True
) -> gb.Matrix:
    """Generates gb.Matrix from list of edges.

    Args:
        size (int): graph size.
        edges (List[Tuple[int, int]]): list of graph edges.
        is_directed (bool): True if graph is directed.

    Returns:
        gb.Matrix: graph.
    """

    graph = gb.Matrix.sparse(gb.types.BOOL, nrows=size, ncols=size)
    for source, target in edges:
        graph[source, target] = True
        if not is_directed:
            graph[target, source] = True

    return graph


def read_graph(path: str) -> gb.Matrix:
    """Read graph from file.

    Args:
        path (str): path to graph.

    Returns:
        gb.Matrix: graph.
    """

    nxm = nx.nx_agraph.read_dot(path)

    return matrix_from_edges(
        nxm.number_of_nodes(),
        [(int(source), int(target)) for source, target in nxm.edges()],
    )


def is_NxN_bool_matrix(graph: gb.Matrix):
    """Checks the graph type and is graph matrix a square matrix.

    Args:
        graph (gb.Matrix): matrix of the graph.

    Raises:
        ValueError: error if graph matrix is not NxN bool matrix.
    """

    if graph.type != gb.BOOL:
        raise ValueError(f"Matrix type was {graph.type}, adjacency matrix expected")
    if not graph.square:
        raise ValueError("Adjacency matrix must be square")


def is_symmetric_matrix(graph: gb.Matrix) -> bool:
    for i, j in zip(graph.I, graph.J):
        x = graph.get(i, j, default=graph.type.default_zero)
        y = graph.get(j, i, default=graph.type.default_zero)
        if x != y:
            return False
    return True


def start_vertex_out_of_range_error(vertex: int) -> ValueError:
    """Creates vertex out of range error.

    Args:
        vertex (int): error vertex.

    Returns:
        ValueError: error.
    """

    return ValueError(f"Start vertex {vertex} is out of range")
