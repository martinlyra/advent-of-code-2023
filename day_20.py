import copy
import math
from typing import Optional
from common import read_file_as_string, test


PULSE_HIGH = 1
PULSE_LOW = 0


def print_events(events: list[tuple[str, int, str]]):
    for src, pulse, dst in events:
        print(f"{src} -{pulse}-> {dst}")


def parse_schematic(string):
    lines = [line for line in str.strip(string).split("\n") if len(line)]

    nodes = {}
    for line in lines:
        parts = [str.strip(p) for p in str.split(line, "->")]
        identifier = parts[0]
        outputs = [str.strip(c) for c in str.split(parts[1], ",")]
        node_type = identifier[0] if not str.isalpha(identifier[0]) else ""
        identifier = identifier[1:] if not str.isalpha(identifier[0]) else identifier

        nodes[identifier] = (node_type, [], outputs)

    for i in list(nodes.keys()):
        for c in nodes[i][2]:
            if c not in nodes:
                nodes[c] = ("out", [], [])
            nodes[c][1].append(i)

    return nodes


def press_button(
    nodes: dict[str, tuple[str, list[str], list[str]]],
    state: Optional[dict[str, int]] = None,
    index: int = 0,
    state_change: Optional[dict[str, dict[int, Optional[int]]]] = None,
):
    node_state: dict[str, int]
    if state is None:
        node_state = {
            n: (PULSE_HIGH if nodes[n][0] == "&" else PULSE_LOW) for n in nodes.keys()
        }
    else:
        node_state = state.copy()

    if state_change is None:
        state_change = {n: {PULSE_LOW: None, PULSE_HIGH: None} for n in nodes.keys()}

    queue: list[tuple[str, str, int]] = [("button", "broadcaster", PULSE_LOW)]
    events: list[tuple[str, int, str]] = []
    while len(queue):
        src, dst, pulse = queue.pop(0)

        events.append((src, pulse, dst))

        before = node_state[dst]
        node_type, inputs, outputs = nodes[dst]
        match node_type:
            case "%":
                if pulse == PULSE_LOW:
                    node_state[dst] = (
                        PULSE_HIGH if node_state[dst] == PULSE_LOW else PULSE_LOW
                    )
                else:
                    continue
            case "&":
                if all(node_state[i] == PULSE_HIGH for i in inputs):
                    node_state[dst] = PULSE_LOW
                else:
                    node_state[dst] = PULSE_HIGH
            case "out":
                node_state[dst] = pulse
                continue
            case _:
                node_state[dst] = pulse

        if node_state[dst] != before:
            v = state_change[dst][node_state[dst]]
            if v is None:
                state_change[dst][node_state[dst]] = index

        queue.extend([(dst, c, node_state[dst]) for c in outputs])
    return events, node_state, state_change


def find_cycle_length(nodes, max_length=1000):
    length = 0
    state = None
    cache = {}
    change = None
    for idx in range(max_length):
        events, state, change = press_button(nodes, state, idx, change)

        highs = sum(p == PULSE_HIGH for _, p, _ in events)
        lows = sum(p == PULSE_LOW for _, p, _ in events)

        key = (hash(tuple(events)), hash(tuple(state.items())))
        if key not in cache:
            cache[key] = (length, highs, lows)
        else:
            break
        length += 1

    return (
        length,
        sum(hs for _, hs, _ in cache.values()),
        sum(ls for _, _, ls in cache.values()),
        try_predict_earliest_low("rx", nodes, change),
    )


def get_pulse_product(nodes, max_length=1000):
    l, hs, ls, c = find_cycle_length(nodes, max_length=max_length)
    return int((hs * ls) * ((max_length / l) ** 2)), c


def try_predict_earliest_low(
    target_node: str,
    nodes: dict[str, tuple[str, list[str], list[str]]],
    state_change: dict[str, dict[int, Optional[int]]],
):
    if target_node not in nodes:
        return None

    def _predict(visting, state) -> Optional[int]:
        changed_when = state_change[visting][state]
        if changed_when is not None:
            return changed_when + 1

        node_type, ins, _ = nodes[visting]
        match node_type:
            case "&":
                return math.prod(
                    [
                        _predict(
                            input_node, PULSE_HIGH if state == PULSE_LOW else PULSE_LOW
                        )
                        or 0
                        for input_node in ins
                    ]
                )
            case "out":
                return math.prod(_predict(input_node, state) or 0 for input_node in ins)
            case _:
                return None

    return _predict(target_node, PULSE_LOW) or None


if __name__ == "__main__":
    examples = [
        parse_schematic(example)
        for example in str.split(
            str.strip(read_file_as_string("input/20-ex.txt")), "\n\n"
        )
        if len(example)
    ]

    test(get_pulse_product(examples[0])[0], 32_000_000)
    test(get_pulse_product(examples[1])[0], 11_687_500)

    task = read_file_as_string("input/20.txt")
    task_nodes = parse_schematic(task)
    print(get_pulse_product(task_nodes, 1000))
    print(get_pulse_product(task_nodes, 5000))
