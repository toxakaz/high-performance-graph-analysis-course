import pytest
from project import msbfs, matrix_from_edges


@pytest.mark.parametrize(
    "size, edges, start, expected_ans",
    [
        (
            3,
            [(0, 1), (1, 2)],
            [0],
            [(0, [-1, 0, 1])],
        ),
        (2, [], [0], [(0, [-1, -2])]),
        (
            4,
            [(0, 1), (2, 3)],
            [0, 2],
            [(0, [-1, 0, -2, -2]), (2, [-2, -2, -1, 2])],
        ),
        (
            6,
            [
                (0, 1),
                (0, 2),
                (1, 4),
                (2, 3),
                (2, 5),
                (3, 2),
                (5, 3),
            ],
            [0, 3],
            [(0, [-1, 0, 0, 2, 1, 2]), (3, [-2, -2, 3, -1, -2, 2])],
        ),
    ],
)
def test_bfs(size, edges, start, expected_ans):
    assert msbfs(matrix_from_edges(size, edges), start) == expected_ans
