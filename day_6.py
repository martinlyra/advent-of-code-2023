from numpy import product
from common import test
from day_5_1 import search_all


EXAMPLE = """
Time:      7  15   30
Distance:  9  40  200
"""

INPUT_PATTERN = r"([\w\- ]+): *((?:\d+ *)+)"


def parse_input(source, pattern):
    return {
        match.group(1): [
            int(number) for number in str.split(match.group(2), " ") if len(number)
        ]
        for match in search_all(source, pattern)
    }


def all_possible_combinations(race):
    time, record = race
    count = 0
    for t in range(time + 1):
        v = t
        d = v * (time - t)
        count += 1 if d > record else 0
    return count


example_input = parse_input(EXAMPLE, INPUT_PATTERN)
test(example_input["Time"], [7, 15, 30])
test(example_input["Distance"], [9, 40, 200])

example_races = zip(example_input["Time"], example_input["Distance"])
test([all_possible_combinations(race) for race in example_races], [4, 8, 9])

with open("input/6-1.txt", "r") as f:
    source_info = "".join(f.readlines())

# Part 1
task_input = parse_input(source_info, INPUT_PATTERN)
print(
    product(
        [
            all_possible_combinations(race)
            for race in zip(task_input["Time"], task_input["Distance"])
        ]
    )
)

# Part 2
task_input = parse_input(source_info.replace(" ", ""), INPUT_PATTERN)
print(
    all_possible_combinations(list(zip(task_input["Time"], task_input["Distance"]))[0])
)
