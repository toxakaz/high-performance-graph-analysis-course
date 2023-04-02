import pytest
import pygraphblas as pb
from project import weight_matrix_from_edges, mssp


@pytest.mark.parametrize(
    "n, edges, start_vector, ans",
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
            [0, 3, 6],
            [
                (0, [0, 3, 10, 8, 4, 5, 10]),
                (3, [2, 5, 4, 0, 6, 7, 12]),
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
            [0, 1, 2, 3],
            [
                (0, [0, 2, 1, None]),
                (1, [None, 0, 3, None]),
                (2, [None, None, 0, None]),
                (3, [42, 42, 43, 0]),
            ],
        ),
    ],
)
def test_mssp(n, edges, start_vector, ans):
    graph = weight_matrix_from_edges(n, edges, type=pb.types.INT64, is_directed=True)
    assert mssp(graph, start_vector) == ans
