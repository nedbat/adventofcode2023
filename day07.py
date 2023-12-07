# https://adventofcode.com/2023/day/07

import collections
import itertools
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
    (1,4,): "Yfour",
    (2,3,): "Xfull",
    (1,1,3,): "Wthree",
    (1,2,2,): "Vpair",
    (1,1,1,2,): "Upair",
    (1,1,1,1,1,): "Thigh",
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


@pytest.mark.parametrize(
    "hand, type",
    [
        ("AAAAA", "Zfive"),
        ("AA8AA", "Yfour"),
        ("23332", "Xfull"),
        ("TTT98", "Wthree"),
        ("23432", "Vpair"),
        ("A23A4", "Upair"),
        ("23456", "Thigh"),
    ],
)
def test_hand_type(hand, type):
    assert Hand(hand).type == type


@pytest.mark.parametrize(
    "hand1, hand2",
    [
        ("2AAAA", "33332"),
        ("77788", "77888"),
        ("32T3K", "KK677"),
        ("KTJJT", "KK677"),
        ("T55J5", "QQQJA"),
    ],
)
def test_hand_compare(hand1, hand2):
    h1 = Hand(hand1)
    h2 = Hand(hand2)
    assert h1 < h2
    assert h2 > h1


def parse_hands(lines, klass=Hand):
    hands = []
    for line in lines:
        cards, bid = line.split()
        hands.append(klass(cards, int(bid)))
    return hands


def test_hand_compare2():
    hands = parse_hands(TEST_INPUT)
    hands.sort()
    print([h.type for h in hands])
    assert [h.cards for h in hands] == ["32T3K", "KTJJT", "KK677", "T55J5", "QQQJA"]


def part1(lines, klass=Hand):
    hands = parse_hands(lines, klass=klass)
    hands.sort()
    return sum(rank * hand.bid for rank, hand in enumerate(hands, start=1))


def test_part1():
    assert part1(TEST_INPUT) == 6440


if __name__ == "__main__":
    answer = part1(file_lines("day07_input.txt"))
    print(f"Part 1: {answer = }")


CARD_STRENGTH2 = {card: num for num, card in enumerate("J23456789TQKA")}


def multi_replace(s, olds, news):
    for old, new in zip(olds, news):
        s = s.replace(old, new)
    return s

# Part 2, first code: find real hands that jokers could represent.

@dataclass
class Hand2:
    cards: str
    bid: int = 0

    def __post_init__(self):
        jokers = self.cards.count("J")
        nonj = list({c for c in self.cards if c != "J"})
        match jokers:
            case 5:
                best = Hand("AAAAA")
            case 4:
                best = Hand(nonj[0] * 5)
            case 3:
                best = Hand(self.cards.replace("J", nonj[0]))
            case 1 | 2:
                candidates = []
                for js in itertools.combinations_with_replacement(nonj, r=jokers):
                    candidates.append(Hand(multi_replace(self.cards, "J" * jokers, js)))
                best = max(candidates)
            case 0:
                best = Hand(self.cards)

        self.type = best.type

    def __lt__(self, other):
        if self.type == other.type:
            strengths1 = [CARD_STRENGTH2[c] for c in self.cards]
            strengths2 = [CARD_STRENGTH2[c] for c in other.cards]
            return strengths1 < strengths2
        else:
            return self.type < other.type


def part2(lines):
    return part1(lines, klass=Hand2)


def test_part2():
    assert part2(TEST_INPUT) == 5905


if __name__ == "__main__":
    answer = part2(file_lines("day07_input.txt"))
    print(f"Part 2: {answer = }")


# Part 2, second code: no need to find real hands, just use counts.

TYPES_2B = {
    (0, (5,)): "Zfive",
    (5, (5,)): "Zfive",
    (0, (1,4,)): "Yfour",
    (1, (1,4,)): "Zfive",
    (4, (1,4,)): "Zfive",
    (1, (1,1,3,)): "Yfour",
    (0, (2,3,)): "Xfull",
    (2, (2,3,)): "Zfive",
    (3, (2,3,)): "Zfive",
    (0, (1,1,3,)): "Wthree",
    (1, (1,1,3,)): "Yfour",
    (3, (1,1,3,)): "Yfour",
    (0, (1,2,2,)): "Vpair",
    (1, (1,2,2,)): "Xfull",
    (2, (1,2,2,)): "Yfour",
    (0, (1,1,1,2,)): "Upair",
    (1, (1,1,1,2,)): "Wthree",
    (2, (1,1,1,2,)): "Wthree",
    (0, (1,1,1,1,1,)): "Thigh",
    (1, (1,1,1,1,1,)): "Upair",
}

@dataclass
class Hand2b:
    cards: str
    bid: int = 0

    def __post_init__(self):
        jokers = self.cards.count("J")
        real_counts = tuple(sorted(collections.Counter(self.cards).values()))
        self.type = TYPES_2B[(jokers, real_counts)]

    def __lt__(self, other):
        if self.type == other.type:
            strengths1 = [CARD_STRENGTH2[c] for c in self.cards]
            strengths2 = [CARD_STRENGTH2[c] for c in other.cards]
            return strengths1 < strengths2
        else:
            return self.type < other.type

def part2b(lines):
    return part1(lines, klass=Hand2b)

def test_part2b():
    assert part2(TEST_INPUT) == 5905


if __name__ == "__main__":
    answer = part2b(file_lines("day07_input.txt"))
    print(f"Part 2b: {answer = }")
