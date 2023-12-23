from common import read_file_as_string, test


def parse_input(puzzle_input):
    return sorted(
        [
            tuple(
                tuple(int(i) for i in str.split(point, ","))
                for point in str.split(line, "~")
            )
            for line in str.split(str.strip(puzzle_input))
            if len(line)
        ],
        key=lambda x: x[0][-1],
    )


def compute_supports(blocks):
    index = dict(enumerate(blocks))
    supports = {i: [] for i in index}
    supported_by = {i: [] for i in index}

    stable = {}
    for idx in index:
        (x1, y1, z1), (x2, y2, z2) = blocks[idx]

        surface = [(x, y) for y in range(y1, y2 + 1) for x in range(x1, x2 + 1)]

        supporters = {}
        while z1 > 1 and len(supporters) < 1:
            for c in [(x, y, z1 - 1) for x, y in surface]:
                if c in stable:
                    supporters[stable[c]] = True
            if len(supporters) < 1:
                z1 -= 1
                z2 -= 1

        spaces = [(x, y, z) for z in range(z1, z2 + 1) for x, y in surface]

        for s in spaces:
            stable[s] = idx

        for support in supporters:
            supports[support].append(idx)
            supported_by[idx].append(support)

    return supports, supported_by


def removable(supports, supported_by):
    return sum(
        [
            not any(len(supported_by[other]) < 2 for other in supports[point])
            for point in supports
        ]
    )


def calculate_chain_reaction(supporting, supported_by):
    def check_fall(index):
        queue = list.copy(supporting[index])
        to_fall = {index: True}

        while len(queue):
            current = queue.pop(0)
            if all(s in to_fall for s in supported_by[current]):
                to_fall[current] = True
                queue.extend(supporting[current])

        return len(to_fall.keys()) - 1  # Exlude the block being removed

    return sum(check_fall(index) for index in supporting)


if __name__ == "__main__":
    example = parse_input(read_file_as_string("input/22-ex.txt"))

    supporting, supported_by = compute_supports(example)

    test(removable(supporting, supported_by), 5)
    test(calculate_chain_reaction(supporting, supported_by), 7)

    task = parse_input(read_file_as_string("input/22.txt"))
    supporting, supported_by = compute_supports(task)

    test(removable(supporting, supported_by), 507)
    test(calculate_chain_reaction(supporting, supported_by), 51733)
