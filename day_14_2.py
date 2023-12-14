from common import test
from day_14_1 import EXAMPLE, calculate_load, parse_map, move_rocks


def print_map(map):
    print("\n" + "\n".join(["".join(line) for line in map]) + "\n")


def cycle(map):
    def _transpose(map):
        return [list(line) for line in list(zip(*map))]

    def _reverse(map):
        return list(reversed(map))

    result = move_rocks(map)  # north
    result = move_rocks(_transpose(result))  # west
    result = move_rocks(_reverse(_transpose(result)))  # south
    result = move_rocks(_reverse(_transpose(result)))  # east
    return _reverse(_transpose(_reverse(result)))


def one_pass(map, cycles=1_000_000_000):
    states: list[int] = []
    maps: list[list] = []
    previous = map
    for iteration in range(cycles):
        current = cycle(previous)

        state_hash = hash(
            frozenset(
                dict.items({i: str.join("", line) for i, line in enumerate(current)})
            )
        )
        if state_hash in states:
            state_index = states.index(state_hash)
            cycle_length = iteration - state_index

            true_index = state_index + ((cycles - iteration) % cycle_length) - 1
            print(f"Stabilized after {iteration} cycles.")
            return maps[true_index]

        states.append(state_hash)
        maps.append(current)
        previous = current
    return previous


if __name__ == "__main__":
    example_moved = cycle(parse_map(EXAMPLE))
    test(calculate_load(one_pass(parse_map(EXAMPLE))), 64)

    with open("input/14.txt", "r") as file:
        source_info = "".join(file.readlines())

    test(calculate_load(one_pass(parse_map(source_info))), 101292)
