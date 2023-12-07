
from common import test


STRENGTH = "23456789TJQKA"

EXAMPLE = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""

def parse_hand(hand):
    return {
        STRENGTH.index(symbol): str.count(hand, symbol)
        for symbol in set(c for c in hand)
    }

def evalute_hand(hand_str):
    sorted_hand = sorted(parse_hand(hand_str).items(), key=lambda x: (x[1], x[0]), reverse=True)

    # cards = [card for card, _ in sorted_hand]
    cards = [STRENGTH.index(c) for c in hand_str]

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

def parse_line(line):
    parts = str.split(line, " ")
    hand = parts[0]
    betting = parts[1]
    return (hand, betting)

def evaluate_game(game):
    rounds = [parse_line(str.strip(line)) for line in str.split(game, "\n") if len(line)]

    evaluated = [(evalute_hand(hand), hand, int(betting)) for hand, betting in rounds]
    ranked = sorted(evaluated, key=lambda x: (x[0], x[2]))

    adjusted_bets = [
        round[2] * (i + 1)
        for i, round in enumerate(ranked)
    ]
    return adjusted_bets

if __name__ == "__main__":
    test(sum(evaluate_game(EXAMPLE)), 6440)

    with open("input/7-1.txt", "r") as f:
        source_info = "".join(f.readlines())

    print(sum(evaluate_game(source_info)))
