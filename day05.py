# https://adventofcode.com/2023/day/05

import itertools
import re
from dataclasses import dataclass

import pytest

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


# Ranges of numbers are represented as a list of [(start, end), (start, end), ...]
# End is not included, as with range().


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
    map_ranges: list[MapRange]

    def __getitem__(self, num):
        for r in self.map_ranges:
            if num in r:
                return r[num]
        else:
            return num

    def map_numbers(self, numbers):
        """Map a set of number ranges through this map, producing a new set of number ranges."""
        to_map = numbers
        result = set()
        for map_range in self.map_ranges:
            next_to_map = []
            sstart = map_range.sstart
            send = map_range.sstart + map_range.rlen
            for start, end in to_map:
                if start < sstart:
                    # The portion of numbers less than the mapped range.
                    next_to_map.append((start, min(end, sstart)))
                if (send >= start) and (end >= sstart):
                    # The ranges overlap.
                    # https://nedbatchelder.com/blog/201310/range_overlap_in_two_compares.html
                    nstart = max(start, sstart)
                    nend = min(end, send)
                    if nstart != nend:
                        mapped = (map_range[nstart], map_range[nend])
                        result.add(mapped)
                if end > send:
                    next_to_map.append((max(start, send), end))
            to_map = next_to_map
        result.update(to_map)
        return result


@dataclass
class Almanac:
    seeds: list[int]
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
            python.append(m.expand(r"seeds=[\1],").replace(" ", ","))
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


def part2(lines):
    almanac = parse_almanac(lines)
    numbers = [(s, s+l) for s, l in itertools.batched(almanac.seeds, 2)]
    for map in almanac.maps:
        numbers = map.map_numbers(numbers)
    smallest = min(numbers)[0]
    return smallest


def test_part2():
    assert part2(TEST_INPUT) == 46


if __name__ == "__main__":
    answer = part2(file_lines("day05_input.txt"))
    print(f"Part 2: {answer = }")
