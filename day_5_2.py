import math
from multiprocessing.pool import ThreadPool
from day_5_1 import EXAMPLE, INPUT_PATTERN, MAP_PATTERN, evaluate_seed, parse_input, parse_map
from common import test

thread_pool = ThreadPool()


def evaluate_sub_range(start, end, mappings):
    least = math.inf
    for seed in range(start, end):
        location, _ = evaluate_seed(seed, mappings)
        least = min(location, least)
    return least
    

def evaluate_seed_range(value, width, mappings):
    results = []
    current = value
    for end in range(value, value+width, max(1, int(width / 128))):
        results.append(thread_pool.apply_async(evaluate_sub_range, (current, end, mappings)))
        current = end
    values = [result.get() for result in results]
    return min(values)


def seed_ranges(input_list):
    ranges = []
    for i in range(int(len(input_list)/2)):
        start = input_list[2*i]
        width = input_list[2*i + 1]
        ranges.append((start, width))
    return ranges

input_list = parse_input(EXAMPLE, INPUT_PATTERN)["seeds"]
mappings = parse_map(EXAMPLE, MAP_PATTERN)

# Parsing tests
test(evaluate_seed_range(79, 14, mappings), 46)
test(seed_ranges(input_list), [(79, 14), (55, 13)])

with open("input/5-1.txt", "r") as f:
    source_info = "".join(f.readlines())

print("File read, parsing.")
input_list = parse_input(source_info, INPUT_PATTERN)["seeds"]
mappings = parse_map(source_info, MAP_PATTERN)

new_input = seed_ranges(input_list)

values = []
for i, pair in enumerate(new_input):
    print(f"Evaluating #{i}, {pair}")
    seed, width = pair
    values.append(evaluate_seed_range(seed, width, mappings))
print(values)
print(min(values))
