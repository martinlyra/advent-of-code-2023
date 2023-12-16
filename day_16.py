from enum import Enum
from functools import reduce
from typing import Optional

from common import test


EXAMPLE = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""

EXAMPLE_ENERGIZED = """
######....
.#...#....
.#...#####
.#...##...
.#...##...
.#...##...
.#..####..
########..
.#######..
.#...#.#..
"""


class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

    def flip(self):
        match self:
            case Direction.UP:
                return Direction.DOWN
            case Direction.DOWN:
                return Direction.UP
            case Direction.RIGHT:
                return Direction.LEFT
            case Direction.LEFT:
                return Direction.RIGHT

def to_grid(map):
    return [c for c in [line for line in str.split(str.strip(map), "\n") if len(line)]]


def trace_path(
    start: tuple[int, int, Direction], map
) -> tuple[
    list[tuple[int, int, Direction]],
    list[list[int]],
    Optional[tuple[int, int, Direction]],
]:
    def is_valid_state(x, y):
        return 0 <= x < len(map[0]) and 0 <= y < len(map)

    def next_step(x, y, dir: Direction):
        match dir:
            case Direction.UP:
                return (x, y - 1)
            case Direction.DOWN:
                return (x, y + 1)
            case Direction.RIGHT:
                return (x + 1, y)
            case Direction.LEFT:
                return (x - 1, y)

    trace = [[0 for _ in row] for row in map]
    x, y, direction = start

    previous = start
    while is_valid_state(x, y):
        tile = map[y][x]
        trace[y][x] += 1

        match tile:
            case ".":
                pass
            case "\\":
                match direction:
                    case Direction.UP:
                        direction = Direction.LEFT
                    case Direction.RIGHT:
                        direction = Direction.DOWN
                    case Direction.LEFT:
                        direction = Direction.UP
                    case Direction.DOWN:
                        direction = Direction.RIGHT
            case "/":
                match direction:
                    case Direction.UP:
                        direction = Direction.RIGHT
                    case Direction.RIGHT:
                        direction = Direction.UP
                    case Direction.LEFT:
                        direction = Direction.DOWN
                    case Direction.DOWN:
                        direction = Direction.LEFT
            case "|":
                match direction:
                    case Direction.DOWN | Direction.UP:
                        pass
                    case Direction.LEFT | Direction.RIGHT:
                        return (
                            [
                                (x, y, Direction.UP),
                                (x, y, Direction.DOWN),
                            ],
                            trace,
                            None,
                        )
            case "-":
                match direction:
                    case Direction.DOWN | Direction.UP:
                        return (
                            [
                                (x, y, Direction.LEFT),
                                (x, y, Direction.RIGHT),
                            ],
                            trace,
                            None,
                        )
                    case Direction.LEFT | Direction.RIGHT:
                        pass

        previous = (x, y, direction)
        step = next_step(x, y, direction)
        x, y = step
    return [], trace, previous


def traverse(map, start=(0, 0, Direction.RIGHT)):
    queue: list[tuple[int, int, Direction]] = [start]
    traces: list[list[list[int]]] = []

    stop_points = [start]
    already_traversed = []
    while len(queue):
        start = queue.pop(0)
        if start in already_traversed:
            continue
        else:
            already_traversed.append(start)
        points, trace, stop = trace_path(start, map)
        queue.extend(points)
        traces.append(trace)
        if stop:
            stop_points.append(stop)

    full_trace = [
        [sum(trace[y][x] for trace in traces) for x in range(len(map[0]))]
        for y in range(len(map))
    ]
    return full_trace, stop_points


def trace_to_energized(trace):
    return "\n".join("".join(["#" if i else "." for i in row]) for row in trace)


def count_energized(trace):
    return reduce(lambda c, row: c + sum((i > 0) for i in row), trace, 0)


def optimize_grid(grid):
    width, height = len(grid[0]), len(grid)
    start_points: dict[tuple[int, int, Direction], int] = {
        k: -1
        for k in reduce(
            lambda l, e: l + e,
            [
                [(0, i, Direction.RIGHT) for i in range(height)],
                [(width - 1, i, Direction.LEFT) for i in range(height)],
                [(i, 0, Direction.DOWN) for i in range(width)],
                [(i, height - 1, Direction.UP) for i in range(width)],
            ],
            []
        )
    }
    for point in start_points:
        if start_points[point] > -1:
            continue

        trace, stops = traverse(grid, point)
        count = count_energized(trace)

        start_points[point] = count
        for stop in stops:
            x,y,d = stop
            p = (x, y, Direction.flip(d))
            if p in start_points:
                start_points[p] = max(count, start_points[p])

    return max(start_points.values())


if __name__ == "__main__":
    trace, _ = traverse(to_grid(EXAMPLE))
    # energized = trace_to_energized(trace)
    # test(energized, EXAMPLE_ENERGIZED.strip())
    test(count_energized(trace), 46)

    with open("input/16.txt", "r") as file:
        source_info = "".join(file.readlines())

    task_trace, _ = traverse(to_grid(source_info))
    # task_energized = trace_to_energized(task_trace)
    # print(task_energized)
    print("Calculating part 1:")
    print(count_energized(task_trace))
    print("Calculating part 2:")
    print(optimize_grid(to_grid(source_info)))
