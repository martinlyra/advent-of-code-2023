
from common import test
from day_7_1 import EXAMPLE, parse_line


STRENGTH = "J23456789TQKA"

def parse_hand(hand):
    return {
        STRENGTH.index(symbol): str.count(hand, symbol)
        for symbol in set(c for c in hand)
    }

def evaluate_hand_value(sorted_hand, cards):
    highest = sorted_hand[0]
    if highest[1] == 5: # five of a kind
        return (6, cards)
    if highest[1] == 4: # four of a kind
        return (5, cards)
    
    second = sorted_hand[1]
    if highest[1] == 3:
        if second[1] == 2: # full house
            return (4, cards)
        else: # three of a kind
            return (3, cards)
    if highest[1] == 2:
        if second[1] == 2: # two pairs
            return (2, cards)
        else: # one pair
            return (1, cards)
        
    # high (highest card)
    return (0, cards)

def evalute_hand(hand_str):
    parsed = parse_hand(hand_str)
    print(parsed)
    sorted_hand = sorted(parsed.items(), key=lambda x: (x[1], x[0]), reverse=True)

    # cards = [card for card, _ in sorted_hand]
    cards = [STRENGTH.index(c) for c in hand_str]

    alt1 = evaluate_hand_value(sorted_hand, cards)

    wildcard_index = STRENGTH.index("J")
    if wildcard_index in parsed and len(parsed) > 1:
        wildcard = parsed.copy()
        wildcard_count = wildcard.pop(STRENGTH.index("J"))
        sorted_wildcard = sorted(wildcard.items(), key=lambda x: (x[1], x[0]), reverse=True)
        sorted_wildcard[0] = (sorted_wildcard[0][0], sorted_wildcard[0][1] + wildcard_count)

        alt2 = evaluate_hand_value(sorted_wildcard, cards)

        if alt1[0] > alt1[0]:
            return alt1
        return alt2
    return alt1

def evaluate_game(game):
    rounds = [parse_line(str.strip(line)) for line in str.split(game, "\n") if len(line)]

    evaluated = [(evalute_hand(hand), hand, int(betting)) for hand, betting in rounds]
    ranked = sorted(evaluated, key=lambda x: (x[0], x[2]))

    adjusted_bets = [
        round[2] * (i + 1)
        for i, round in enumerate(ranked)
    ]
    return adjusted_bets

test(sum(evaluate_game(EXAMPLE)), 5905)

with open("input/7-1.txt", "r") as f:
    source_info = "".join(f.readlines())

print(sum(evaluate_game(source_info)))
