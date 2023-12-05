import re
from common import test, read_file

EXAMPLE = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

def parse_game_round(line: str) -> dict[str, int]:
    tots = [l.strip() for l in line.split(",")]
    game_round = {}
    for cube in tots:
        num, color = cube.split(" ")[:2]
        game_round[color] = int(num)
    return game_round

def evaluate_game(line: str):
    game = line[line.find(":")+1:].strip()
    rounds = str.split(game, ";")
    
    minimums: dict[str, int] = {key: 0 for key in EXAMPLE}
    for round in rounds:
        cubes = parse_game_round(round)
        for key in cubes:
            minimums[key] = max(minimums[key], cubes[key])

    power_set = 1
    for num in [num for _, num in minimums.items()]:
        power_set *= int(num)
    return power_set

test(evaluate_game("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"), 48)
test(evaluate_game("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue"), 12)
test(evaluate_game("Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red"), 1560)
test(evaluate_game("Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red"), 630)
test(evaluate_game("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"), 36)

powers = [evaluate_game(line) for line in read_file("input/2-1.txt")]
print(sum(powers))
