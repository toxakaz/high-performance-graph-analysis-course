import pytest
import pygraphblas as pb
from project import weight_matrix_from_edges, apsp


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
            [
                (0, [0, 3, 10, 8, 4, 5, 10]),
                (1, [14, 0, 7, 12, 1, 2, 7]),
                (2, [None, None, 0, None, None, 5, None]),
                (3, [2, 5, 4, 0, 6, 7, 12]),
                (4, [None, None, 6, None, 0, 1, None]),
                (5, [None, None, 5, None, None, 0, None]),
                (6, [7, 10, 1, 5, 8, 6, 0]),
            ],
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
            [
                (0, [0, 2, 1, None]),
                (1, [None, 0, 3, None]),
                (2, [None, None, 0, None]),
                (3, [42, 42, 43, 0]),
            ],
        ),
    ],
)
def test_apsp(n, edges, ans):
    graph = weight_matrix_from_edges(n, edges, type=pb.types.INT64, is_directed=True)
    assert apsp(graph) == ans
