# https://adventofcode.com/2023/day/07

import collections
from dataclasses import dataclass

import pytest

from helpers import *

TEST_INPUT = string_lines(
    """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""
)

CARD_STRENGTH = {card: num for num, card in enumerate("23456789TJQKA")}

TYPES = {
    (5,): "Zfive",
    (1, 4,): "Yfour",
    (2, 3,): "Xfull",
    (1, 1, 3,): "Wthree",
    (1, 2, 2,): "Vpair",
    (1, 1, 1, 2,): "Upair",
    (1, 1, 1, 1, 1,): "Thigh",
}

@dataclass
class Hand:
    cards: str
    bid: int = 0

    def __post_init__(self):
        self.type = TYPES[tuple(sorted(collections.Counter(self.cards).values()))]

    def __lt__(self, other):
        if self.type == other.type:
            strengths1 = [CARD_STRENGTH[c] for c in self.cards]
            strengths2 = [CARD_STRENGTH[c] for c in other.cards]
            return strengths1 < strengths2
        else:
            return self.type < other.type

@pytest.mark.parametrize("hand, type", [
    ("AAAAA", "Zfive"),
    ("AA8AA", "Yfour"),
    ("23332", "Xfull"),
    ("TTT98", "Wthree"),
    ("23432", "Vpair"),
    ("A23A4", "Upair"),
    ("23456", "Thigh"),
])
def test_hand_type(hand, type):
    assert Hand(hand).type == type


@pytest.mark.parametrize("hand1, hand2", [
    ("2AAAA", "33332"),
    ("77788", "77888"),
    ("32T3K", "KK677"),
    ("KTJJT", "KK677"),
    ("T55J5", "QQQJA"),
])
def test_hand_compare(hand1, hand2):
    h1 = Hand(hand1)
    h2 = Hand(hand2)
    assert h1 < h2
    assert h2 > h1


def parse_hands(lines):
    hands = []
    for line in lines:
        cards, bid = line.split()
        hands.append(Hand(cards, int(bid)))
    return hands

def test_hand_compare2():
    hands = parse_hands(TEST_INPUT)
    hands.sort()
    print([h.type for h in hands])
    assert [h.cards for h in hands] == ["32T3K", "KTJJT", "KK677", "T55J5", "QQQJA"]

def part1(lines):
    hands = parse_hands(lines)
    hands.sort()
    return sum(rank * hand.bid for rank, hand in enumerate(hands, start=1))


def test_part1():
    assert part1(TEST_INPUT) == 6440


if __name__ == "__main__":
    answer = part1(file_lines("day07_input.txt"))
    print(f"Part 1: {answer = }")


# def part2(lines):
#     ...
#
#
# def test_part2():
#     assert part2(TEST_INPUT) == 123456
#
#
#
# if __name__ == "__main__":
#     answer = part2(file_lines("day07_input.txt"))
#     print(f"Part 2: {answer = }")
