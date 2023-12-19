import math
from common import read_file_as_string, test
from day_19_1 import Operation, Rule, parse_state


def count_combinations(share: dict[str, tuple[int, int]]):
    return math.prod((u - l + 1) for l, u in share.values())


def generate_chains(rules: dict[str, Rule]):
    def _visit(rule: Rule, values: dict[str, tuple[int, int]]):
        current_share = values
        to_visit = []
        for condition in rule.conditions:
            this_share = current_share.copy()

            tl, tu = this_share[condition.variable]
            cl, cu = current_share[condition.variable]
            match condition.operation:
                case Operation.LESSER_THAN:
                    tu = min(condition.threshold - 1, tu)
                    cl = max(cl, tu + 1)

                case Operation.GREATER_THAN:
                    tl = max(condition.threshold + 1, tl)
                    cu = min(cu, tl - 1)

            this_share[condition.variable] = (tl, tu)
            current_share[condition.variable] = (cl, cu)

            to_visit.append((condition.target, this_share))
        to_visit.append((rule.wildcard, current_share))

        chains = []
        for visit, share in to_visit:
            if visit in ["A", "R"]:
                chains.append(([rule.identifier, visit], count_combinations(share)))
            else:
                chains.extend(
                    [
                        ([rule.identifier, *chain], N)
                        for chain, N in _visit(rules[visit], share)
                    ]
                )
        return chains

    return _visit(
        rules["in"], {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}
    )


def find_combinations(rules):
    return sum(N for chain, N in generate_chains(rules) if chain[-1] == "A")


if __name__ == "__main__":
    example = read_file_as_string("input/19-ex.txt")
    example_rules, _ = parse_state(example)

    test(find_combinations(example_rules), 167409079868000)

    task = read_file_as_string("input/19.txt")
    task_rules, _ = parse_state(task)
    print(find_combinations(task_rules))
