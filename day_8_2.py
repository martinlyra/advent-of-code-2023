from math import lcm

from common import test
from day_8_1 import parse_tree, walk_tree


EXAMPLE = """
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""


def walk_tree_ghost(source):
    tree = parse_tree(source)

    nodes = [node for node in tree if str.endswith(node, "A")]
    return lcm(
        *[walk_tree(source, node, lambda n: str.endswith(n, "Z")) for node in nodes]
    )


if __name__ == "__main__":
    test(walk_tree_ghost(EXAMPLE), 6)

    with open("input/8-1.txt", "r") as f:
        source_info = "".join(f.readlines())

    print(walk_tree_ghost(source_info))
