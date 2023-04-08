import pytest
from project import matrix_from_edges, bfs


@pytest.mark.parametrize(
    "size, edges, start, expected_ans",
    [
        (
            4,
            [(0, 1), (1, 2), (2, 3)],
            0,
            [0, 1, 2, 3],
        ),
        (3, [(0, 1), (1, 2), (2, 0)], 0, [0, 1, 2]),
        (
            6,
            [(0, 1), (0, 2), (1, 4), (2, 3), (2, 5), (3, 2), (5, 3)],
            0,
            [0, 1, 1, 2, 2, 2],
        ),
        (
            6,
            [(0, 1), (0, 2), (1, 4), (2, 3), (2, 5), (3, 2), (5, 3)],
            3,
            [-1, -1, 1, 0, -1, 2],
        ),
    ],
)
def test_bfs(size, edges, start, expected_ans):
    assert bfs(matrix_from_edges(size, edges), start) == expected_ans
