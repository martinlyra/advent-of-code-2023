from collections import defaultdict
from functools import reduce
import math
import networkx

from common import test, read_file_as_string


def parse_puzzle(string):
    def f(line):
        key, connections = str.split(line, ": ")
        return [(key, other) for other in str.split(connections, " ")]

    return reduce(
        lambda l, e: l + e,
        [f(line) for line in str.split(str.strip(string), "\n")],
        [],
    )


def edges_to_adjacent(edges):
    result = defaultdict(dict)
    for a, b in edges:
        result[a][b] = {"weight": 1}
    return result


def split_graph(edges):
    g = networkx.from_dict_of_dicts(edges_to_adjacent(edges))
    clusters = next(networkx.community.girvan_newman(g))
    return math.prod(len(cluster) for cluster in clusters)


if __name__ == "__main__":
    edges = parse_puzzle(read_file_as_string("input/25-ex.txt"))
    test(split_graph(edges), 54)

    task_edges = parse_puzzle(read_file_as_string("input/25.txt"))
    print(split_graph(task_edges))
