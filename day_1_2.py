import re as regex
from typing import Generator

from common import read_file, test

numbers = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def regex_matches(
    pattern: regex.Pattern, line: str
) -> Generator[regex.Match, None, None]:
    position = 0
    while True:
        match = pattern.search(line, pos=position)
        if match is None:
            break
        yield match
        position = match.end(0)


def locate_digits(line: str) -> list[tuple[int, int]]:
    digits = []
    for i in range(len(line)):
        c = line[i]
        if str.isdigit(c):
            digits.append((i, c))
    return digits


def locate_words(line: str, dictionary=numbers) -> list[tuple[int, int]]:
    digits = []

    for key in dictionary:
        for regex_match in regex_matches(regex.compile(key), line):
            position = regex_match.start(0)
            digits.append((position, str(dictionary[key])))

    return digits


def parse_line(line: str) -> int:
    digits = []
    digits.extend(locate_digits(line))
    digits.extend(locate_words(line))

    cleaned = [pair[1] for pair in sorted(digits, key=lambda x: x[0])]

    num = int(cleaned[0] + cleaned[-1])
    return num


test(parse_line("two1nine"), 29)
test(parse_line("eightwothree"), 83)
test(parse_line("abcone2threexyz"), 13)
test(parse_line("4nineeightseven2"), 42)
test(parse_line("zoneight234"), 14)
test(parse_line("7pqrstsixteen"), 76)


nums = []
for line in read_file("input/1-1.txt"):
    nums.append(parse_line(line))

print(sum(nums))
