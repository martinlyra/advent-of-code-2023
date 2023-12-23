

from functools import reduce
from common import read_file_as_string, test
from day_16 import to_grid


def neighbors(grid, x, y):
    w, h = len(grid[0]), len(grid)

    match grid[y][x]:
        case '>':
            return [(x+1, y)]
        case '<':
            return [(x-1, y)]
        case 'v':
            return [(x, y+1)]
        case '^':
            return [(x, y-1)]
        case _:
            pass

    def is_valid_tile(x, y, c):
        return (
            0 <= x < w and 0 <= y < h and grid[y][x] not in (c, '#')
        )

    return [
        t for t in [
            (x-1, y) if is_valid_tile(x-1, y, '>') else None,
            (x+1, y) if is_valid_tile(x+1, y, '<') else None,
            (x, y-1) if is_valid_tile(x, y-1, 'v') else None,
            (x, y+1) if is_valid_tile(x, y+1, '^') else None,
        ]
        if t
    ]


def find_paths(grid):
    cache = {}

    def _find_path(start) -> list[int]:
        if start not in cache:
            cache[start] = _path(start)
        return cache[start]

    def _path(start) -> list[int]:
        visited = {start: True}
        current = start

        def ns():
            return [n for n in neighbors(grid, *current) if n not in visited]

        forward = ns()
        length = 1
        while len(forward) == 1:
            visited[current] = True
            current = forward[0]
            length += 1
            forward = ns()

        if len(forward) == 0:
            return [length - 1]

        return [
            length + other_path_length
            for other_path_length in reduce(
                lambda l, ps: l + ps,
                [_find_path(n) for n in forward],
                [],
            )
        ]

    return sorted(_path((1, 0)), reverse=True)


if __name__ == "__main__":
    example = to_grid(read_file_as_string("input/23-ex.txt"))
    test(find_paths(example), [94, 90, 86, 82, 82, 74])

    task = to_grid(read_file_as_string("input/23.txt"))
    print(find_paths(task)[0])
