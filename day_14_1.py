import copy

from common import test


EXAMPLE = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""

EXAMPLE_MOVED = """
OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#....
"""


def parse_map(map) -> list[list[str]]:
    return [list(line) for line in str.strip(map).split("\n")]


def move_rocks(map) -> list[list[str]]:
    new_map = copy.deepcopy(map)

    for i in range(1, len(new_map)):
        for j in range(0, len(new_map[0])):
            if new_map[i][j] != "O":
                continue

            k = i
            while k > 0 and new_map[k - 1][j] == ".":
                k -= 1

            if k != i:
                tmp = new_map[i][j]
                new_map[i][j] = "."
                new_map[k][j] = tmp
    return new_map


def calculate_load(map) -> int:
    return sum(
        sum(len(map) - i for j in range(len(map[0])) if map[i][j] == "O")
        for i in range(len(map))
    )


if __name__ == "__main__":
    example_moved = move_rocks(parse_map(EXAMPLE))
    test(
        "\n" + "\n".join(["".join(line) for line in example_moved]) + "\n",
        EXAMPLE_MOVED,
    )
    test(calculate_load(example_moved), 136)

    with open("input/14.txt", "r") as file:
        source_info = "".join(file.readlines())

    moved_task = move_rocks(parse_map(source_info))
    test(calculate_load(moved_task), 113525)
