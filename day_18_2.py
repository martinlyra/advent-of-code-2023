from functools import reduce
from common import read_file_as_string, test


DIRECTION_HEX_MAP = {"0": "R", "1": "D", "2": "L", "3": "U"}


DIRECTION_SHIFT = {
    "U": (0, -1),
    "D": (0, 1),
    "L": (-1, 0),
    "R": (1, 0),
}


def parse_instruction_line(line: str):
    hex = line.split(" ")[2][1:-1]
    return DIRECTION_HEX_MAP[hex[-1]], int(hex[1:-1], base=16)


def create_vertex(p, i):
    direction, count = i
    shift = DIRECTION_SHIFT[direction]
    return p[0] + shift[0] * count, p[1] + shift[1] * count


def count_dugout(raw_instructions):
    instructions = [
        parse_instruction_line(line)
        for line in str.split(str.strip(raw_instructions), "\n")
        if len(line)
    ]

    vertices = reduce(
        lambda l, x: l + [create_vertex(l[-1], x)], instructions, [(0, 0)]
    )
    length = int(reduce(lambda l, x: l + x[1], instructions, 0) / 2)

    # Shoelace formula
    area = int(
        abs(
            sum(
                (x1 * y2 - x2 * y1) / 2
                for (x1, y1), (x2, y2) in zip(vertices, vertices[1:])
            )
        )
    )
    return area + length + 1


if __name__ == "__main__":
    example = read_file_as_string("input/18-ex.txt")
    test(count_dugout(example), 952408144115)

    task = read_file_as_string("input/18.txt")
    test(count_dugout(task), 42708339569950)
