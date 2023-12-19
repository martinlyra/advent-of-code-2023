from enum import Enum
import re

from common import read_file_as_string, test
from day_5_1 import search_all


RULE_PATTERN = re.compile(r"(\w+){([^\n]+)}")
CONDITION_PATTERN = re.compile(r"(\w)(<|>)(\d+):(\w+)")
PART_PATTERN = re.compile(r"(\w)=(\d+)")


class Operation(Enum):
    GREATER_THAN = 0
    LESSER_THAN = 1

    @staticmethod
    def from_string(string):
        match string:
            case r"<":
                return Operation.LESSER_THAN
            case r">":
                return Operation.GREATER_THAN
            case _:
                raise RuntimeError(f"Unknown operation '{string}'")


class RuleCondition:
    variable: str
    operation: Operation
    threshold: int
    target: str


class Rule:
    def __init__(self, identifier, conditions, wildcard) -> None:
        self.identifier: str = identifier
        self.conditions: list[RuleCondition] = conditions
        self.wildcard: str = wildcard

    @staticmethod
    def parse_rule(string):
        match = re.match(RULE_PATTERN, string)
        if match is None:
            raise RuntimeError(f"No regex match on {string}")

        identifier = match.group(1)
        conditions = match.group(2).split(",")

        parsed_conditions = []
        for condition in conditions[:-1]:
            parsed_condition = re.match(CONDITION_PATTERN, condition)
            if not parsed_condition:
                print(f"Failed to parse '{condition}'")
                continue

            rc = RuleCondition()
            rc.variable = parsed_condition.group(1)
            rc.operation = Operation.from_string(parsed_condition.group(2))
            rc.threshold = int(parsed_condition.group(3))
            rc.target = parsed_condition.group(4)

            parsed_conditions.append(rc)

        return Rule(identifier, parsed_conditions, conditions[-1])


def parse_state(string):
    sections = [section for section in str.strip(string).split("\n\n") if len(section)]
    rules = {
        rule.identifier: rule
        for rule in [Rule.parse_rule(rule) for rule in str.split(sections[0], "\n")]
    }
    parts = [
        {
            match.group(1): int(match.group(2))
            for match in search_all(part, PART_PATTERN)
        }
        for part in str.split(sections[1], "\n")
    ]

    return rules, parts


def evaluate_part(rules, part):
    def evaluate_conditions(conditions):
        for c in conditions:
            b, t = evaluate_condition(c)
            if b:
                return t
        return None

    def evaluate_condition(condition: RuleCondition):
        match condition.operation:
            case Operation.GREATER_THAN:
                return (
                    part[condition.variable] > condition.threshold,
                    condition.target,
                )
            case Operation.LESSER_THAN:
                return (
                    part[condition.variable] < condition.threshold,
                    condition.target,
                )
        return (False, "R")

    current_node = "in"
    chain = [current_node]
    while current_node not in ["A", "R"]:
        rule: Rule = rules[current_node]
        evaluated = evaluate_conditions(rule.conditions)
        if evaluated:
            current_node = evaluated
        else:
            current_node = rule.wildcard
        chain.append(current_node)
    return (part if current_node == "A" else None, chain)


def evaluate_state(rules, parts):
    return sum(sum(part.values()) for part in parts if evaluate_part(rules, part)[0])


if __name__ == "__main__":
    example = read_file_as_string("input/19-ex.txt")
    example_rules, example_parts = parse_state(example)
    test(
        evaluate_part(example_rules, example_parts[0])[1],
        ["in", "qqz", "qs", "lnx", "A"],
    )
    test(
        evaluate_part(example_rules, example_parts[1])[1],
        ["in", "px", "rfg", "gd", "R"],
    )
    test(
        evaluate_part(example_rules, example_parts[2])[1],
        ["in", "qqz", "hdj", "pv", "A"],
    )
    test(
        evaluate_part(example_rules, example_parts[3])[1],
        ["in", "px", "qkq", "crn", "R"],
    )
    test(evaluate_part(example_rules, example_parts[4])[1], ["in", "px", "rfg", "A"])

    test(evaluate_state(example_rules, example_parts), 19114)

    task = read_file_as_string("input/19.txt")
    print(evaluate_state(*parse_state(task)))
