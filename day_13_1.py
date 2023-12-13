from typing import Optional
from common import test


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


def parse_map(map_str) -> list[list[str]]:
    patterns = []
    pattern = []
    for line in str.strip(map_str).split("\n"):
        if len(line):
            pattern.append(list(line))
        else:
            patterns.append(pattern)
            pattern = []
    if len(pattern):
        patterns.append(pattern)
    return patterns


def find_mirror(pattern) -> tuple[Optional[int], Optional[int]]:
    vs, hs = find_mirrors(pattern)
    return (vs[0] if len(vs) else None, hs[0] if len(hs) else None) 

def find_mirrors(pattern) -> tuple[list[int], list[int]]:
    def _find(pattern) -> list[int]:
        n = len(pattern)
        candidates = [
            (i, i + 1)
            for i, line in enumerate(pattern)
            if i < (n - 1) and line == pattern[i + 1]
        ]
        mirrors = [
            u
            for l, u in candidates
            if all(pattern[l - i] == pattern[u + i] for i in range(0, min(u, n - u)))
        ]
        return mirrors

    return _find(list(zip(*pattern))), _find(pattern)


def calculate_patterns(patterns):
    return calculate_mirrors([find_mirror(pattern) for pattern in patterns])


def calculate_mirrors(mirrors):
    return sum((v if v else 0) + ((h * 100) if h else 0) for v, h in mirrors)


if __name__ == "__main__":
    examples = parse_map(EXAMPLE)
    test(find_mirror(examples[0]), ((5, None)))
    test(find_mirror(examples[1]), (None, 4))
    test(calculate_patterns(examples), 405)

    with open("input/13.txt", "r") as file:
        source_info = "".join(file.readlines())

    tasks = parse_map(source_info)
    test(calculate_patterns(tasks), 27664)
