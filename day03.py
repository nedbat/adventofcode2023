# https://adventofcode.com/2023/day/3

import re
from dataclasses import dataclass

from helpers import *

TEST_INPUT = string_lines("""\
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
""")


@dataclass
class Number:
    x: int
    y: int
    ndigits: int
    num: int

    def neighboring_locations(self):
        x0 = self.x - 1
        x1 = self.x + self.ndigits
        return set(
            (
                *[(xx, self.y - 1) for xx in range(x0, x1 + 1)],
                (x0, self.y),
                (x1, self.y),
                *[(xx, self.y + 1) for xx in range(x0, x1 + 1)],
            )
        )


def find_numbers(lines):
    for lineno, line in enumerate(lines):
        for match in re.finditer(r"\d+", line):
            yield Number(match.start(), lineno, len(match[0]), int(match[0]))


def find_symbols(lines):
    for lineno, line in enumerate(lines):
        for match in re.finditer(r"[^.\d\s]", line):
            yield (match.start(), lineno, match[0])


def test_find_numbers():
    assert list(find_numbers(TEST_INPUT)) == [
        Number(x=0, y=0, ndigits=3, num=467),
        Number(x=5, y=0, ndigits=3, num=114),
        Number(x=2, y=2, ndigits=2, num=35),
        Number(x=6, y=2, ndigits=3, num=633),
        Number(x=0, y=4, ndigits=3, num=617),
        Number(x=7, y=5, ndigits=2, num=58),
        Number(x=2, y=6, ndigits=3, num=592),
        Number(x=6, y=7, ndigits=3, num=755),
        Number(x=1, y=9, ndigits=3, num=664),
        Number(x=5, y=9, ndigits=3, num=598),
    ]


def test_find_symbols():
    assert list(find_symbols(TEST_INPUT)) == [
        (3, 1, "*"),
        (6, 3, "#"),
        (3, 4, "*"),
        (5, 5, "+"),
        (3, 8, "$"),
        (5, 8, "*"),
    ]


def test_neighboring_locations():
    assert Number(3, 4, 3, 123).neighboring_locations() == {
        (2, 3),
        (3, 3),
        (4, 3),
        (5, 3),
        (6, 3),
        (2, 4),
        (6, 4),
        (2, 5),
        (3, 5),
        (4, 5),
        (5, 5),
        (6, 5),
    }


def part1(lines):
    numbers = list(find_numbers(lines))
    symbols = list(find_symbols(lines))
    symbol_spots = set((x, y) for x, y, s in symbols)
    part_numbers = []
    for num in numbers:
        if num.neighboring_locations() & symbol_spots:
            part_numbers.append(num)
    return sum(pnum.num for pnum in part_numbers)


def test_part1():
    assert part1(TEST_INPUT) == 4361


if __name__ == "__main__":
    answer = part1(file_lines("day03_input.txt"))
    print(f"Part 1: {answer = }")


def gears(lines):
    numbers = list(find_numbers(lines))
    stars = [(x, y) for x, y, s in find_symbols(lines) if s == "*"]
    for star in stars:
        adjacent_nums = []
        possible_rows = {star[1] - 1, star[1], star[1] + 1}
        for num in numbers:
            if num.y not in possible_rows:
                continue
            if star in num.neighboring_locations():
                adjacent_nums.append(num)
        if len(adjacent_nums) == 2:
            yield tuple(anum.num for anum in adjacent_nums)


def test_gears():
    assert list(gears(TEST_INPUT)) == [(467, 35), (755, 598)]


def part2(lines):
    return sum(g1 * g2 for g1, g2 in gears(lines))


def test_part2():
    assert part2(TEST_INPUT) == 467835


if __name__ == "__main__":
    answer = part2(file_lines("day03_input.txt"))
    print(f"Part 2: {answer = }")
