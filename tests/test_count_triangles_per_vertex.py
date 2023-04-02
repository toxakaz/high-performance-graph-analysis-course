import pytest
from project import matrix_from_edges, count_triangles_per_vertex


@pytest.mark.parametrize(
    "size, edges, expected_ans",
    [
        (
            3,
            [(0, 1), (0, 2), (1, 2)],
            [1, 1, 1],
        ),
        (
            4,
            [(0, 1), (0, 3), (1, 2), (2, 3)],
            [0, 0, 0, 0],
        ),
        (
            4,
            [(0, 1), (0, 2), (0, 3), (1, 2), (2, 3)],
            [2, 1, 2, 1],
        ),
        (
            7,
            [(0, 1), (0, 2), (1, 2), (1, 3), (1, 4), (3, 4), (3, 5), (4, 6), (5, 6)],
            [1, 2, 1, 1, 1, 0, 0],
        ),
    ],
)
def test_count_triangles_per_vertex(size, edges, expected_ans):
    assert (
        count_triangles_per_vertex(matrix_from_edges(size, edges, is_directed=False))
        == expected_ans
    )
