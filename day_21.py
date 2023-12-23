import math
from common import read_file_as_string, test
from day_16 import to_grid
from day_17 import DIRECTION_SHIFT, DOWN, LEFT, RIGHT, UP


DIRECTIONS = [UP, RIGHT, DOWN, LEFT]


def neighbors_4(x, y):
    return [
        (
            x + DIRECTION_SHIFT[direction][0],
            y + DIRECTION_SHIFT[direction][1],
        )
        for direction in DIRECTIONS
    ]


def neighbors_bounded(map, x, y):
    for px, py in neighbors_4(x, y):
        if not (0 <= px < len(map[0]) and 0 <= py < len(map)):
            continue
        if map[py][px] == "#":
            continue
        yield (px, py)


def neighbors_wrapping(map, x, y):
    for px, py in neighbors_4(x, y):
        if map[py % len(map)][px % len(map[0])] == "#":
            continue
        yield (px, py)


def bfs(map, start, max_distance, get_neighbors):
    queue: list[tuple[int, tuple[int, int]]] = [(0, start)]
    visited = {}
    total = 0
    parity = max_distance % 2

    while len(queue):
        d, (x, y) = queue.pop(0)
        if d > max_distance:
            return total

        if (x, y) in visited:
            continue

        if d % 2 == parity:
            total += 1

        visited[(x, y)] = True
        for px, py in get_neighbors(map, x, y):
            queue.append((d + 1, (px, py)))
    return total


def starting_position(map):
    for i in range(len(map)):
        if "S" in map[i]:
            return (str.index(map[i], "S"), i)
    raise RuntimeError("Failed to find starting position in map.")


def part_1(map, steps):
    return bfs(map, starting_position(map), steps, neighbors_bounded)


# Solution using quadratic sequence formula as suggested
# in the megathread at the subreddit
def part_2(map, steps):
    h = len(map)
    remainder = steps % h
    start = starting_position(map)

    vs = [bfs(map, start, remainder + i * h, neighbors_wrapping) for i in range(3)]

    d1 = vs[1] - vs[0]
    d2 = vs[2] - vs[1]
    d3 = d2 - d1

    A = d3 // 2
    B = d1 - 3 * A
    C = vs[0] - B - A

    f = math.ceil(steps / h)
    return A * f**2 + B * f + C


if __name__ == "__main__":
    example = to_grid(read_file_as_string("input/21-ex.txt"))
    test(part_1(example, 6), 16)

    task = to_grid(read_file_as_string("input/21.txt"))
    print(part_1(task, 64))
    print(part_2(task, 26501365))
