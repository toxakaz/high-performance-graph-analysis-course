import pytest
import pygraphblas as pb
from project import weight_matrix_from_edges, sssp


@pytest.mark.parametrize(
    "n, edges, ans",
    [
        (
            7,
            [
                (0, 3, 1),
                (0, 8, 3),
                (1, 1, 4),
                (1, 7, 6),
                (2, 5, 5),
                (3, 2, 0),
                (3, 4, 2),
                (4, 1, 5),
                (5, 5, 2),
                (6, 1, 2),
                (6, 5, 3),
                (6, 8, 4),
            ],
            [0, 3, 10, 8, 4, 5, 10],
        ),
        (
            4,
            [
                (0, 2, 1),
                (1, 3, 2),
                (0, 1, 2),
                (3, 42, 0),
                (3, 42, 1),
            ],
            [0, 2, 1, None],
        ),
    ],
)
def test_sssp(n, edges, ans):
    graph = weight_matrix_from_edges(n, edges, type=pb.types.INT64, is_directed=True)
    assert sssp(graph, 0) == ans
