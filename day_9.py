from common import test


EXAMPLE = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""


def compute_layer(ints: list[int]) -> list[int]:
    return [ints[i + 1] - ints[i] for i in range(len(ints) - 1)]


def compute_stack(ints: list[int]) -> list[list[int]]:
    stack = [ints]
    current = ints
    while any(i != 0 for i in current):
        current = compute_layer(current)
        stack.append(current)
    return stack


def extend_stack(stack: list[list[int]], forwards=1, backwards=0) -> list[list[int]]:
    stack = stack.copy()
    for _ in range(forwards):
        stack[-1].append(0)
        for i in range(2, len(stack) + 1):
            layer = stack[-i]
            layer.append(layer[-1] + stack[-(i - 1)][-1])
    for _ in range(backwards):
        stack[-1].insert(0, 0)
        for i in range (2, len(stack) + 1):
            layer = stack[-i]
            layer.insert(0, layer[0] - stack[-(i - 1)][0])
    return stack


def predict_mirage(history) -> tuple[int, int]:
    ints = [int(p) for p in str.strip(history).split(" ") if len(p)]
    stack = extend_stack(compute_stack(ints), 1, 1)
    return (stack[0][-1], stack[0][0])


if __name__ == "__main__":
    examples = [predict_mirage(example) for example in str.strip(EXAMPLE).split("\n")]
    test(examples, [(18, -3), (28, 0), (68, 5)])
    test(sum(ex[0] for ex in examples), 114)
    test(sum(ex[1] for ex in examples), 2)

    with open("input/9-1.txt", "r") as f:
        source_info = "".join(f.readlines())

    mirages = [predict_mirage(history) for history in str.strip(source_info).split("\n")]
    print(sum(mi[0] for mi in mirages))
    print(sum(mi[1] for mi in mirages))
