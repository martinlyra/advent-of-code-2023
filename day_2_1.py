import re
from common import test, read_file

EXAMPLE = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

TASK = EXAMPLE

def get_game_id(line) -> int:
    match = re.match(re.compile(r"Game (\d+):"), line)
    if match is None:
        raise RuntimeError("Matched none on line")
    return int(match.group(1))

def parse_game_round(line: str) -> dict[str, int]:
    tots = [l.strip() for l in line.split(",")]
    game_round = {}
    for cube in tots:
        num, color = cube.split(" ")[:2]
        game_round[color] = int(num)
    return game_round

def evaluate_game(line: str, game_bag: dict[str, int]):
    game = line[line.find(":")+1:].strip()
    rounds = str.split(game, ";")
    
    for round in rounds:
        cubes = parse_game_round(round)
        for key in cubes:
            if game_bag[key] < cubes[key]:
                return False
    return True

test(evaluate_game("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green", EXAMPLE), True)
test(evaluate_game("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue", EXAMPLE), True)
test(evaluate_game("Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red", EXAMPLE), False)
test(evaluate_game("Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red", EXAMPLE), False)
test(evaluate_game("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green", EXAMPLE), True)

test(get_game_id("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"), 1)
test(get_game_id("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue"), 2)
test(get_game_id("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"), 5)

ids = []
for line in read_file("input/2-1.txt"):
    is_possible = evaluate_game(line, TASK)
    if is_possible:
        ids.append(get_game_id(line))

print(sum(ids))
