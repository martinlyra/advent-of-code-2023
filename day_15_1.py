from functools import reduce

from common import test


EXAMPLE = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"


def parts(string):
    return str.split(str.strip(string), ",")


def hash(string):
    return reduce(lambda s, c: int(((s + ord(c)) * 17) % 256), string, 0)


def calculate_hash(parts):
    return [hash(part) for part in parts]


if __name__ == "__main__":
    example_parts = calculate_hash(parts(EXAMPLE))
    test(example_parts, [30, 253, 97, 47, 14, 180, 9, 197, 48, 214, 231])
    test(sum(example_parts), 1320)

    with open("input/15.txt", "r") as file:
        source_info = "".join(file.readlines())

    print(sum(calculate_hash(parts(source_info))))
