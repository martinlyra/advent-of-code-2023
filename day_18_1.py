from functools import reduce
import math
from common import read_file_as_string, test


DIRECTION_SHIFT = {
    "U": (0, -1),
    "D": (0, 1),
    "L": (-1, 0),
    "R": (1, 0),
}


def parse_instruction_line(line: str):
    parts = line.split(" ")
    return parts[0], int(parts[1]), parts[2]


def find_range(numbers):
    return reduce(
        lambda l, x: (min(l[0], x), max(l[1], x)),
        numbers,
        (math.inf, -math.inf),
    )


def find_size(instructions):
    horizontial = reduce(
        lambda l, x: l
        + [(l[-1] + (x[1] if x[0] == "R" else (-x[1] if x[0] == "L" else 0)))],
        [(i, c) for i, c, _ in instructions if i in ["L", "R"]],
        [0],
    )
    vertical = reduce(
        lambda l, x: l
        + [(l[-1] + (x[1] if x[0] == "D" else (-x[1] if x[0] == "U" else 0)))],
        [(i, c) for i, c, _ in instructions if i in ["D", "U"]],
        [0],
    )
    horizontial_range = find_range(horizontial)
    vertical_range = find_range(vertical)

    width = int(horizontial_range[1] - horizontial_range[0]) + 1
    height = int(vertical_range[1] - vertical_range[0]) + 1
    starting_point = -horizontial_range[0], -vertical_range[0]
    return starting_point, width, height


def dig(instructions):
    lines = [
        parse_instruction_line(line)
        for line in str.strip(instructions).split("\n")
        if len(line)
    ]

    # Calculate size
    starting_point, width, height = find_size(lines)

    # Start digging the outline
    print("Digging outline")
    grid = [["." for _ in range(width)] for _ in range(height)]
    cursor = starting_point
    for instruction in lines:
        direction, count, _ = instruction

        x, y = cursor
        shift_x, shift_y = DIRECTION_SHIFT[direction]
        for _ in range(count):
            x, y = x + shift_x, y + shift_y
            grid[y][x] = "#"

        cursor = x, y

    # Dig the interior
    print("Digging interior")
    fill_point = (0, 0)
    for i, row in enumerate(grid):
        if list.count(row, "#") == 2:
            fill_point = list.index(row, "#") + 1, i
            break

    queue = [fill_point]
    visited = {}
    while len(queue):
        x, y = queue.pop(0)
        if (x,y) in visited:
            continue
        visited[(x,y)] = True

        grid[y][x] = "#"

        neighbors = [(x + i, y + j) for i in range(-1, 2) for j in range(-1, 2)]
        for neighbor in neighbors:
            nx, ny = neighbor
            if grid[ny][nx] == ".":
                queue.append(neighbor)

    return grid


def count_dugout(instructions):
    return sum(list.count(row, '#') for row in dig(instructions))


if __name__ == "__main__":
    example = read_file_as_string("input/18-ex.txt")
    test(count_dugout(example), 62)

    task = read_file_as_string("input/18.txt")
    test(count_dugout(task), 53844)
