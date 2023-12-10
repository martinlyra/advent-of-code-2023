import copy
from functools import reduce
import random
import time
from common import test
from day_10_1 import parse_map


EXAMPLE = """
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""

EXAMPLE_1 = """
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""

EXAMPLE_2 = """
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
"""

EXAMPLE_3 = """
..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
..........
"""

LOOP_TILE = "H"


def print_outline(outline):
    print("")
    for line in outline:
        print("".join(line))
    print("")


def cube(x, y, height, width):
    return [
        (i, j)
        for i in range(max(x - 1, 0), min(height, x + 2))
        for j in range(max(y - 1, 0), min(width, y + 2))
    ]


def explode_map(map):
    _, _, nodes = parse_map(map)

    height = len(nodes)
    width = len(nodes[0])
    outline = [["."] * (width * 2 + 1)]
    for i in range(height):
        row = ["."]
        below = ["."]
        for j in range(width):
            node = nodes[i][j]
            if node and len(node.unconnected()) == 0:
                if "south" in node.connectors and node.connectors["south"]:
                    below.extend(["|", "."])
                else:
                    below.extend([".", "."])
                if "east" in node.connectors and node.connectors["east"]:
                    row.extend([node.symbol, "-"])
                else:
                    row.extend([node.symbol, "."])
            else:
                row.extend([".", "."])
                below.extend([".", "."])
        outline.append(row)
        outline.append(below)
    return outline


def implode_outline(outline):
    return [
        [tile for j, tile in enumerate(row) if j % 2 == 1]
        for i, row in enumerate(outline)
        if i % 2 == 1
    ]


def flood_scan(area: list[list[str]], height, width):
    result = copy.deepcopy(area)

    queue: list[tuple[int, int]] = [(0, 0)]
    while len(queue):
        x, y = queue.pop(0)
        neighbors = cube(x, y, height, width)
        for neighbor in neighbors:
            i, j = neighbor
            if area[i][j] == LOOP_TILE:
                result[i][j] = LOOP_TILE
            elif result[i][j] == "O":
                continue
            else:
                result[i][j] = "O"
                queue.append((i, j))

    return result


def check_enclosed(map):
    outline = [
        [LOOP_TILE if tile != "." else tile for tile in row] for row in explode_map(map)
    ]

    width = len(outline[0])
    height = len(outline)

    first_pass = flood_scan(outline, height, width)

    be = []
    enclosed = 0
    for row in implode_outline(first_pass):
        r = []
        for tile in row:
            if tile == LOOP_TILE:
                r.append(".")
                continue
            if tile == "O":
                r.append(" ")
                continue
            r.append("I")
            enclosed += 1
        be.append(r)

    with open(f"day-10-preview.txt", "wt") as f:
        for line in be:
            f.write("".join(line))
            f.write("\n")

    return enclosed


if __name__ == "__main__":
    test(check_enclosed(EXAMPLE), 8)
    test(check_enclosed(EXAMPLE_1), 10)
    test(check_enclosed(EXAMPLE_2), 4)

    with open("input/10-1.txt", "r") as f:
        source_info = "".join(f.readlines())

    print(check_enclosed(source_info))
