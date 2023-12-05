import math
from common import test


EXAMPLE = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""


KNOWN_SYMBOLS = "*#+$&%-@=/"


class Symbol:
    def __init__(self, row: int, col: int) -> None:
        self.position_row: int = row
        self.position_col: int = col


class NumberSymbol(Symbol):
    def __init__(self, row, col, value) -> None:
        super().__init__(row, col)
        self.value = value
        self.width = math.floor(math.log10(value)) + 1

        self.adjacent = []

    def register_adjacent(self, part):
        self.adjacent.append(part)

    def has_adjacent(self) -> bool:
        return len(self.adjacent) > 0


class PartSymbol(Symbol):
    def __init__(self, row: int, col: int, c) -> None:
        super().__init__(row, col)
        self.symbol = c
        self.adjacent = []
    
    def __str__(self) -> str:
        return f"<PartSymbol, row={self.position_row}, col={self.position_col}, symbol='{self.symbol}'>"
    
    def register_adjacent(self, numsym: NumberSymbol):
        numsym.register_adjacent(self)
        self.adjacent.append(numsym)


class LineIterator:
    def __init__(self, line) -> None:
        self.line = line
        self.index = 0

    def rewind(self):
        self.index -= 1

    def next(self) -> tuple[int, str]:
        if self.index < len(self.line):
            i = self.index
            char = self.line[self.index]
            self.index += 1
            return (i, char)
        else:
            raise StopIteration


def is_within(min, val, max):
    return min <= val <= max


def take_number(iterator: LineIterator, char, row, col) -> NumberSymbol:
    buffer = char
    try:
        while True:
            c: str
            _, c = iterator.next()
            if c.isdigit():
                buffer += c
            else:
                iterator.rewind()
                break
    except StopIteration:
        pass
    return NumberSymbol(row, col, int(buffer))


def parse_line(row: int, line: str) -> list[Symbol]:
    line = line.strip()

    symbols = []
    column = 0
    it = LineIterator(line)
    try:
        while True:
            column, char = it.next()
            if char == ".":
                continue
            if char.isdigit():
                symbols.append(take_number(it, char, row, column))
                continue
            if char in KNOWN_SYMBOLS:
                symbols.append(PartSymbol(row, column, char))
                continue
            raise RuntimeError(f"Unknown symbol: '{char}'")
    except StopIteration:
        pass

    return symbols


def evaluate_number_symbol(
    i, symbol: NumberSymbol, symbol_map: dict[int, list[Symbol]]
) -> int:
    i_min = 0
    i_max = len(symbol_map.keys()) - 1

    self_j_min = symbol.position_col - 1
    self_j_max = symbol.width + symbol.position_col

    def check_row(j):
        if i_min <= j <= i_max:
            syms = symbol_map[j]
            for sym in syms:
                if isinstance(sym, PartSymbol):
                    if is_within(self_j_min, sym.position_col, self_j_max):
                        sym.register_adjacent(symbol)
                        return True
        return False

    if any(
        [
            check_row(i - 1),
            check_row(i),
            check_row(i + 1),
        ]
    ):
        return True
    return False


def parse_schematic(schematic: str) -> tuple[dict[int, list[Symbol]], list[NumberSymbol], list[PartSymbol]]:
    lines = schematic.strip().split("\n")

    numbers = []
    parts = []
    symbol_map = {}
    for i, line in enumerate(lines):
        parsed = parse_line(i, line)
        for symbol in parsed:
            if isinstance(symbol, NumberSymbol):
                numbers.append(symbol)
            elif isinstance(symbol, PartSymbol):
                parts.append(symbol)
        symbol_map[i] = parsed

    for i in symbol_map:
        symbols = symbol_map[i]
        for symbol in symbols:
            if isinstance(symbol, NumberSymbol):
                evaluate_number_symbol(i, symbol, symbol_map)

    return symbol_map, numbers, parts

def evaluate_schematic_sum(schematic: str) -> int:
    _, numbers, _ = parse_schematic(schematic)

    nums = []

    for num in numbers:
        if num.has_adjacent():
            nums.append(num.value)

    return sum(nums)


def evaluate_schematic_gears(schematic: str) -> int:
    _, _, parts = parse_schematic(schematic)
    
    nums = []
    for part in parts:
        if len(part.adjacent) == 2:
            nums.append(part.adjacent[0].value * part.adjacent[1].value)

    return sum(nums)


test(evaluate_schematic_sum(EXAMPLE), 4361)  # Part 1 example
test(evaluate_schematic_gears(EXAMPLE), 467835)  # Part 2 example

with open("input/3-1.txt", "r") as f:
    schematic = "".join(f.readlines())

test(evaluate_schematic_sum(schematic), 527446)
print(evaluate_schematic_gears(schematic))
