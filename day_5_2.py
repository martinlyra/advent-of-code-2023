from day_5_1 import EXAMPLE, INPUT_PATTERN, MAP_PATTERN, map_lookup, parse_input, parse_map
from common import test


def seed_ranges(input_list):
    return [(input_list[i * 2], input_list[i * 2 + 1]) for i in range(int(len(input_list) / 2))]


def search_range_overlaps(start, end, value_map):
    overlaps = []
    for entry in value_map:
        width = entry[2]
        source_start = entry[1]
        source_end = source_start + width - 1

        if source_start <= start or end <= end:
            new_start = max(start, source_start)
            new_end = min(source_end, end)

            diff = new_end - new_start

            if diff > 0:
                overlaps.append((new_start, new_end))

    # No overlap, 1:1 ratio
    if len(overlaps):
        return overlaps

    return [(start, end)]


def search_overlaps(seed_range, mapping: dict):
    seed_start, seed_width = seed_range
    seed_end = seed_start + seed_width - 1

    tests = [(seed_start, seed_end)]
    for map_name in list(mapping.keys()):
        mapped = []
        value_map = mapping[map_name]
        for test in tests:
            start, end = test
            mapped.extend(search_range_overlaps(start, end, value_map))

        tests = [
            (
                map_lookup(s, value_map),
                map_lookup(e, value_map),
            )
            for s, e in mapped
        ]
    return tests


def evaluate_seed_range(seed_range, mappings: dict):
    return min(result[0] for result in search_overlaps(seed_range, mappings))


input_list = parse_input(EXAMPLE, INPUT_PATTERN)["seeds"]
mappings = parse_map(EXAMPLE, MAP_PATTERN)

# Parsing tests
test(seed_ranges(input_list), [(79, 14), (55, 13)])
test(evaluate_seed_range((79, 14), mappings), 46)

with open("input/5-1.txt", "r") as f:
    source_info = "".join(f.readlines())

print("File read, parsing.")
input_list = parse_input(source_info, INPUT_PATTERN)["seeds"]
mappings = parse_map(source_info, MAP_PATTERN)

print(min([evaluate_seed_range(seed, mappings) for seed in seed_ranges(input_list)]))
