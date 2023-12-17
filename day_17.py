import math
from queue import PriorityQueue

from common import read_file_as_string, test

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


DIRECTION_SHIFT = {UP: (0, -1), RIGHT: (1, 0), DOWN: (0, 1), LEFT: (-1, 0)}


AVAILABLE_TURNS = {
    UP: [LEFT, RIGHT],
    DOWN: [RIGHT, LEFT],
    RIGHT: [UP, DOWN],
    LEFT: [DOWN, UP],
}


def to_int_grid(str_map):
    return [list(map(int, str.strip(row))) for row in str.split(str.strip(str_map), "\n")]


def minimize_path(grid, minimum_distance = 0, maximum_distance = 3):
    w, h = len(grid[0]), len(grid)
    distance_cache = {
        (c, r): [math.inf, math.inf, math.inf, math.inf]
        for c in range(w)
        for r in range(h)
    }
    distance_cache[(0, 0)] = [0, 0, 0, 0]

    pq = PriorityQueue()
    pq.put((0, (0, 0), RIGHT))
    pq.put((0, (0, 0), DOWN))

    while not pq.empty():
        heat_loss, position, direction = pq.get()

        if heat_loss > distance_cache[position][direction]:
            continue

        x, y = position
        for i in range(maximum_distance):
            x, y = (x + DIRECTION_SHIFT[direction][0], y + DIRECTION_SHIFT[direction][1])
            current_position = (x, y)

            if not (0 <= x < w and 0 <= y < h):
                break

            heat_loss += grid[y][x]

            if i < (minimum_distance - 1):
                continue

            for turn in AVAILABLE_TURNS[direction]:
                if heat_loss < distance_cache[current_position][turn]:
                    distance_cache[current_position][turn] = heat_loss
                    pq.put((heat_loss, current_position, turn))

    return min(distance_cache[(w - 1, h - 1)])


if __name__ == "__main__":
    example = to_int_grid(read_file_as_string("input/17-ex.txt"))
    test(minimize_path(example), 102)
    test(minimize_path(example, 4, 10), 94)

    task_grid = to_int_grid(read_file_as_string("input/17.txt"))
    print("Part 1:", minimize_path(task_grid))
    print("Part 2:", minimize_path(task_grid, 4, 10))
