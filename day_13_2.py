import copy
from functools import reduce
from typing import Optional
from common import test
from day_13_1 import calculate_mirrors, find_mirror, find_mirrors, parse_map


EXAMPLE = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""


def desmudged(pattern) -> list[list[list[str]]]:
    def _desmudge(pattern, i, j):
        p = copy.deepcopy(pattern)
        p[i][j] = "." if p[i][j] == "#" else "#"
        return p

    return [
        _desmudge(pattern, i, j)
        for i in range(len(pattern))
        for j in range(len(pattern[0]))
    ]


def desmudged_mirror(pattern) -> tuple[Optional[int], Optional[int]]:
    original = find_mirror(pattern)
    mirrors = [
        mirror
        for mirror in reduce(
            lambda l, e: l + [(v, None) for v in e[0]] + [(None, h) for h in e[1]],
            [find_mirrors(candidate) for candidate in desmudged(pattern)],
            [],
        )
        if not (all(m is None for m in mirror) or mirror == original)
    ]
    return mirrors[0] if len(mirrors) else original


if __name__ == "__main__":
    examples = parse_map(EXAMPLE)
    test(calculate_mirrors([desmudged_mirror(pattern) for pattern in examples]), 400)

    with open("input/13.txt", "r") as file:
        source_info = "".join(file.readlines())

    tasks = parse_map(source_info)
    smudged = [desmudged_mirror(pattern) for pattern in tasks]
    test(calculate_mirrors(smudged), 33991)
