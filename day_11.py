from math import comb, sqrt
from common import test


EXAMPLE = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""


def galaxy_locations(grid):
    return [
        (x, y)
        for y, row in enumerate(grid)
        for x, tile, in enumerate(row)
        if tile == "#"
    ]


def unoccupied_space(grid):
    galaxies = galaxy_locations(grid)
    return [x for x in range(len(grid[0])) if x not in [gx for gx, _ in galaxies]], [
        y for y in range(len(grid)) if y not in [gy for _, gy in galaxies]
    ]


def galaxy_distance(a, b, unoccupied, empty_space):
    def expension_offset(axis):
        return sum(
            (empty_space - 1) if is_between(a[axis], b[axis], t) else 0
            for t in unoccupied[axis]
        )

    return manhattan_distance(a, b) + expension_offset(0) + expension_offset(1)


def is_between(a, b, u):
    return min(a, b) < u < max(a, b)


def manhattan_distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    return sum(abs(b[i] - a[i]) for i in range(len(a)))


def calculate_distances(map, empty_space=2):
    grid = str.strip(map).split("\n")
    galaxies = galaxy_locations(grid)
    connections = [
        (a, b) for a in range(len(galaxies)) for b in range(a, len(galaxies)) if a != b
    ]
    assert comb(len(galaxies), 2) == len(connections)

    unoccupied = unoccupied_space(grid)

    distances = {
        (a, b): galaxy_distance(galaxies[a], galaxies[b], unoccupied, empty_space)
        for a, b in connections
    }
    return distances.values()


if __name__ == "__main__":
    test(unoccupied_space(str.strip(EXAMPLE).split("\n")), ([2, 5, 8], [3, 7]))
    test(sum(calculate_distances(EXAMPLE)), 374)

    with open("input/11-1.txt", "r") as f:
        source_info = "".join(f.readlines())

    test(sum(calculate_distances(source_info)), 9724940)
    test(sum(calculate_distances(source_info, 1_000_000)), 569052586852)
