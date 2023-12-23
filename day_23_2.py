

import copy
from functools import reduce
import math
from common import read_file_as_string, test
from day_16 import to_grid


def neighbors(grid, x, y):
    w, h = len(grid[0]), len(grid)

    def is_valid_tile(x, y):
        return (
            0 <= x < w and 0 <= y < h and grid[y][x] not in ('#')
        )

    return [
        t for t in [
            (x-1, y) if is_valid_tile(x-1, y) else None,
            (x+1, y) if is_valid_tile(x+1, y) else None,
            (x, y-1) if is_valid_tile(x, y-1) else None,
            (x, y+1) if is_valid_tile(x, y+1) else None,
        ]
        if t
    ]


def parse_map(grid):
    segments = []
    nodes = []

    def ns(current, visited):
        return [n for n in neighbors(grid, *current) if n not in visited]

    queue = [(None, (1, 0))]

    def pathfind(start_node, start):
        visited = {start_node: True, start: True}
        current = start

        forward = ns(current, visited)
        length = 1
        while len(forward) == 1:
            visited[current] = True
            current = forward[0]

            if current in nodes:
                segments.append((start_node, current, length + 1))
                return

            length += 1
            forward = ns(current, visited)

        if len(forward) == 0:
            segments.append((start_node, None, length-1))
            return

        nodes.append(current)
        segments.append((start_node, current, length))

        queue.extend(
            [
                (current, n)
                for n in forward
            ]
        )

    while len(queue):
        pathfind(*queue.pop())

    return dict(reduce(
        lambda l, x: l + [((x[0], x[1]), x[2]), ((x[1], x[0]), x[2])],
        [(
            s if s else 'start',
            t if t else 'end',
            w,
        )
            for s, t, w in segments
        ],
        [],))


def dfs(edges):
    adjacent = {}
    for (s, t) in edges:
        if s not in adjacent:
            adjacent[s] = []
        adjacent[s].append(t)

    def _dfs(node_index, visited):
        visited = visited.copy()
        visited[node_index] = True

        if node_index == 'end':
            return [(0, list(visited.keys()))]

        return reduce(
            lambda l, e: l + e,
            [
                [
                    (edges[node_index, adj] + d, chain)
                    for d, chain in _dfs(adj, visited)
                ]
                for adj in adjacent[node_index]
                if adj not in visited
            ],
            [],
        )

    distance, _ = max(_dfs('start', {}))
    return distance


if __name__ == "__main__":
    example = to_grid(read_file_as_string("input/23-ex.txt"))
    test(dfs(parse_map(example)), 154)

    task = to_grid(read_file_as_string("input/23.txt"))
    test(dfs(parse_map(task)), 6802)
