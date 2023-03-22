import pygraphblas as gb
from typing import List

__all__ = ["bfs"]


def bfs(graph: gb.Matrix, start: int) -> List[int]:
    """BFS on a directed graph.

    Args:
        graph (gb.Matrix): NxN bool matrix of the graph
        start (int): bfs start index (from 0 to N - 1)

    Returns:
        List[int]: a list, where for each vertex it is indicated at what step it is reachable.
            The starting vertex is reachable at the 0 step,
            if the vertex is not reachable, then the value of the corresponding cell is -1.
    """
    if graph.type != gb.BOOL:
        raise ValueError(f"Matrix type was {graph.type}, adjacency matrix expected")
    if not graph.square:
        raise ValueError("Adjacency matrix must be square")
    if start < 0 or start >= graph.nrows:
        raise ValueError(f"Start vertex {start} is out of range")

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
