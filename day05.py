# https://adventofcode.com/2023/day/05

import re
from dataclasses import dataclass

from helpers import *

TEST_INPUT = string_lines(
    """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""
)


@dataclass
class MapRange:
    dstart: int
    sstart: int
    rlen: int

    def __contains__(self, num):
        return num in range(self.sstart, self.sstart + self.rlen)

    def __getitem__(self, num):
        return num - self.sstart + self.dstart


@dataclass
class Map:
    ranges: list[MapRange]

    def __getitem__(self, num):
        for r in self.ranges:
            if num in r:
                return r[num]
        else:
            return num

@dataclass
class Almanac:
    seeds: set[int]
    maps: list[Map]

    def __getitem__(self, num):
        for map in self.maps:
            num = map[num]
        return num


def parse_almanac(lines):
    """Transform the input into Python, and evaluate it!"""
    python = []
    python.append("Almanac(")
    nmaps = 0
    for line in lines:
        if m := re.fullmatch("seeds: (.*)", line):
            python.append(m.expand(r"seeds={\1},").replace(" ", ","))
            python.append("maps=[")
        elif m := re.search("map:$", line):
            if nmaps:
                python.append("]),")
            python.append("Map([")
            nmaps += 1
        elif m := re.fullmatch(r"(\d+) (\d+) (\d+)", line):
            python.append(m.expand(r"MapRange(\1, \2, \3),"))
        else:
            python.append(line)
    python.append("])")
    python.append("]")
    python.append(")")
    return eval("\n".join(python))


def test_one_range():
    almanac = parse_almanac(TEST_INPUT)
    results = [almanac.maps[0][num] for num in [79, 14, 55, 13]]
    assert results == [81, 14, 57, 13]


def test_almanac():
    almanac = parse_almanac(TEST_INPUT)
    results = [almanac[num] for num in [79, 14, 55, 13]]
    assert results == [82, 43, 86, 35]


def part1(lines):
    almanac = parse_almanac(lines)
    results = [almanac[num] for num in almanac.seeds]
    return min(results)


def test_part1():
    assert part1(TEST_INPUT) == 35


if __name__ == "__main__":
    answer = part1(file_lines("day05_input.txt"))
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
#     answer = part2(file_lines("day05_input.txt"))
#     print(f"Part 2: {answer = }")
