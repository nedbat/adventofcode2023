# https://adventofcode.com/2023/day/04

import re
from dataclasses import dataclass

from helpers import *

TEST_INPUT = string_lines(
    """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""
)


@dataclass
class ScratchCard:
    id: int
    winning: set[int]
    have: set[int]

    @classmethod
    def parse(cls, line):
        card, _, rest = line.partition(": ")
        winning, _, have = rest.partition(" | ")
        return cls(
            id=int(card.split()[-1]),
            winning=set(map(int, winning.split())),
            have=set(map(int, have.split())),
        )

    def matches(self):
        return len(self.winning & self.have)

    def points(self):
        if self.matches() == 0:
            return 0
        else:
            return 2 ** (self.matches() - 1)


def test_parse():
    assert ScratchCard.parse("Card 17: 45 32 20 | 45 34 23 1") == ScratchCard(
        id=17, winning={20, 32, 45}, have={34, 23, 1, 45}
    )


def part1(lines):
    cards = [ScratchCard.parse(line) for line in lines]
    return sum(card.points() for card in cards)


def test_part1():
    assert part1(TEST_INPUT) == 13


if __name__ == "__main__":
    answer = part1(file_lines("day04_input.txt"))
    print(f"Part 1: {answer = }")


def part2(lines):
    cards = [ScratchCard.parse(line) for line in lines]
    counts = dict.fromkeys([c.id for c in cards], 1)
    for card in cards:
        id = card.id
        num_cards = counts[id]
        matches = card.matches()
        for next_id in range(id + 1, id + matches + 1):
            counts[next_id] += num_cards
    return sum(counts.values())


def test_part2():
    assert part2(TEST_INPUT) == 30


if __name__ == "__main__":
    answer = part2(file_lines("day04_input.txt"))
    print(f"Part 2: {answer = }")
