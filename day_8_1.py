import itertools
import re
from common import test
from day_5_1 import search_all


EXAMPLE = """
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

EXAMPLE_2 = """
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""

START_NODE = "AAA"
TARGET_NODE = "ZZZ"
NODE_PATTERN = r"(\w+) = \((\w+), (\w+)\)"


def parse_tree(source):
    return {
        match.group(1): (match.group(2), match.group(3))
        for match in search_all(source, re.compile(NODE_PATTERN))
    }


def walk_tree(source, start, end_predicate):
    instruction = itertools.cycle([c for c in str.split(str.strip(source), "\n")[0]])
    tree = parse_tree(source)

    next_node = start
    chain = [next_node]
    while not end_predicate(next_node):
        direction = next(instruction)
        left, right = tree[next_node]
        if direction == "L":
            next_node = left
        elif direction == "R":
            next_node = right
        chain.append(next_node)
    return len(chain) - 1


def walk_tree_simple(source):
    return walk_tree(source, START_NODE, lambda n: n == TARGET_NODE)


if __name__ == "__main__":
    test(walk_tree_simple(EXAMPLE), 2)
    test(walk_tree_simple(EXAMPLE_2), 6)

    with open("input/8-1.txt", "r") as f:
        source_info = "".join(f.readlines())

    print(walk_tree_simple(source_info))
