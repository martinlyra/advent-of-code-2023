import re
from typing import Optional
from common import test


EXAMPLE = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

INPUT_PATTERN = r"([\w\- ]+): ((?:\d+ ?)+)"
MAP_PATTERN = r"([\w\- ]+) map:\n((?:\d+ \d+ \d+\n?)+)"


def search_all(source, pattern) -> list[re.Match]:
    matches = []

    regex = re.compile(pattern)
    position = 0
    while position < len(source):
        match: Optional[re.Match] = regex.search(source, position)
        if match is None:
            return matches
        matches.append(match)
        position = match.end()
    return matches


def parse_input(source, pattern):
    match: Optional[re.Match] = re.compile(pattern).search(source)
    if match is None:
        raise RuntimeError(f"Pattern /{pattern}/ was not found.")

    name = match.group(1)
    numbers = match.group(2)

    return {name: [int(number) for number in str.split(numbers, " ")]}


def parse_map(source, pattern):
    objects = {}
    for match in search_all(source, pattern):
        name = match.group(1)
        lines = match.group(2)

        parts = str.split(lines, "\n")
        maps = [[int(number) for number in str.split(part)] for part in parts if len(part)]

        objects[name] = maps
    return objects


def map_lookup(value, value_map):
    for entry in value_map:
        width = entry[2]
        destination = entry[0]
        source = entry[1]

        if not (source <= value < source + width):
            continue

        diff = value - source
        return destination + diff
    return value


def evaluate_seed(value, mappings):
    chain = [value]

    current = value
    for key in mappings:
        value_map = mappings[key]
        current = map_lookup(current, value_map)
        chain.append(current)

    return current, chain


if __name__ == "__main__":
    input_list = parse_input(EXAMPLE, INPUT_PATTERN)["seeds"]
    mappings = parse_map(EXAMPLE, MAP_PATTERN)

    # Parsing tests
    test(input_list, [79, 14, 55, 13])
    test(mappings["seed-to-soil"], [[50, 98, 2], [52, 50, 48]])

    test(map_lookup(50, mappings["seed-to-soil"]), 52)
    test(map_lookup(10, mappings["seed-to-soil"]), 10)

    test(evaluate_seed(79, mappings), (82, [79, 81, 81, 81, 74, 78, 78, 82]))
    test(evaluate_seed(14, mappings), (43, [14, 14, 53, 49, 42, 42, 43, 43]))
    test(evaluate_seed(55, mappings), (86, [55, 57, 57, 53, 46, 82, 82, 86]))
    test(evaluate_seed(13, mappings), (35, [13, 13, 52, 41, 34, 34, 35, 35]))

    with open("input/5-1.txt", "r") as f:
        source_info = "".join(f.readlines())

    print("File read, parsing.")
    input_list = parse_input(source_info, INPUT_PATTERN)["seeds"]
    mappings = parse_map(source_info, MAP_PATTERN)

    print("File parsed, evaluating.")
    locations = [evaluate_seed(seed, mappings) for seed in input_list]
    print("Finding minimum.")
    print(min(locations))
