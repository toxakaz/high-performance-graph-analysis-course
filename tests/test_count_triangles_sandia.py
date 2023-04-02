import pytest
from project import matrix_from_edges, count_triangles_sandia


@pytest.mark.parametrize(
    "size, edges, expected_ans",
    [
        (
            3,
            [(0, 1), (0, 2), (1, 2)],
            1,
        ),
        (
            4,
            [(0, 1), (0, 3), (1, 2), (2, 3)],
            0,
        ),
        (
            4,
            [(0, 1), (0, 2), (0, 3), (1, 2), (2, 3)],
            2,
        ),
        (
            7,
            [(0, 1), (0, 2), (1, 2), (1, 3), (1, 4), (3, 4), (3, 5), (4, 6), (5, 6)],
            2,
        ),
        (
            6,
            [
                (0, 1),
                (0, 2),
                (0, 3),
                (1, 3),
                (1, 4),
                (2, 3),
                (2, 5),
                (3, 4),
                (3, 5),
                (4, 5),
            ],
            5,
        ),
    ],
)
def test_count_triangles_sandia(size, edges, expected_ans):
    assert (
        count_triangles_sandia(matrix_from_edges(size, edges, is_directed=False))
        == expected_ans
    )
