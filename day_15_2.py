from common import test
from day_15_1 import EXAMPLE, parts, hash


def parse_instruction(string):
    label = "".join([c for c in string if str.isalpha(c)])
    return label, string[len(label)]


def parse_string(string):
    ps = parts(string)
    boxes = {i: {} for i in range(256)}
    for p in ps:
        label, operation = parse_instruction(p)
        position = hash(label)

        box = boxes[position]
        match operation:
            case "=":
                box[label] = int(p[-1])
            case "-":
                if label in box:
                    box.pop(label)
    return boxes


def calculate_focal(boxes):
    return sum(
        sum(
            (position + 1) * (slot + 1) * value
            for slot, value in enumerate(boxes[position].values())
        )
        for position in boxes
    )


if __name__ == "__main__":
    test(calculate_focal(parse_string(EXAMPLE)), 145)
    with open("input/15.txt", "r") as file:
        source_info = "".join(file.readlines())

    print(calculate_focal(parse_string(source_info)))
