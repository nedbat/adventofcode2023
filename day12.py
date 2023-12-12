# https://adventofcode.com/2023/day/12

import itertools
import re

from helpers import *

import pytest


TEST_INPUT = string_lines(
    """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""
)

def parse(lines):
    for line in lines:
        springs, sizes = line.split(" ")
        sizes = list(map(int, sizes.split(",")))
        yield springs, sizes

def check_record(springs, sizes):
    spring_chunks = [chunk for chunk in re.split(r"\.+", springs) if chunk]
    return list(map(len, spring_chunks)) == sizes

@pytest.mark.parametrize("record", [
    "#.#.### 1,1,3",
    ".#...#....###. 1,1,3",
    ".#.###.#.###### 1,3,1,6",
])
def test_check_record_good(record):
    springs, sizes = next(parse([record]))
    assert check_record(springs, sizes)

@pytest.mark.parametrize("record", [
    "#.#.#### 1,1,3",
    ".#...#....###. 1,2,3",
    ".#.###.#.###.## 1,3,1,6",
])
def test_check_record_bad(record):
    springs, sizes = list(parse([record]))[0]
    assert not check_record(springs, sizes)


def replace_all(text, repch, replacements):
    rep_it = iter(replacements)
    return "".join(next(rep_it) if ch == repch else ch for ch in text)

@pytest.mark.parametrize("text, repl, result", [
    ("a?b?c?d", "XYZ", "aXbYcZd"),
    ("?b??", "XYZ", "XbYZ"),
])
def test_replace_all(text, repl, result):
    assert replace_all(text, "?", repl) == result


def orders(hashes, dots, sofar=""):
    if hashes == 0 and dots == 0:
        yield sofar
    else:
        if hashes:
            yield from orders(hashes-1, dots, sofar + "#")
        if dots:
            yield from orders(hashes, dots-1, sofar + ".")


def count_possibilities(springs, sizes):
    unknown = springs.count("?")
    missing_damaged = sum(sizes) - springs.count("#")
    total = 0
    for replacement_order in orders(missing_damaged, unknown - missing_damaged):
        replaced_springs = replace_all(springs, "?", replacement_order)
        if check_record(replaced_springs, sizes):
            total += 1
    return total

@pytest.mark.parametrize("record, arrangements", [
    ("???.### 1,1,3", 1),
    (".??..??...?##. 1,1,3", 4),
    ("?#?#?#?#?#?#?#? 1,3,1,6", 1),
    ("????.#...#... 4,1,1", 1),
    ("????.######..#####. 1,6,5", 4),
    ("?###???????? 3,2,1", 10),
])
def test_count_possibilities(record, arrangements):
    springs, sizes = next(parse([record]))
    assert count_possibilities(springs, sizes) == arrangements


def part1(lines):
    total = 0
    for springs, sizes in parse(lines):
        total += count_possibilities(springs, sizes)
    return total


def test_part1():
    assert part1(TEST_INPUT) == 21


if __name__ == "__main__":
    answer = part1(file_lines("day12_input.txt"))
    print(f"Part 1: {answer = }")


def part2(lines):
    # The simple way to do it, will never finish.
    # The test input didn't finish in 10 minutes.
    total = 0
    for springs, sizes in parse(lines):
        springs *= 5
        sizes *= 5
        total += count_possibilities(springs, sizes)
    return total



def test_part2():
    assert part2(TEST_INPUT) == 525152



if __name__ == "__main__":
    answer = part2(file_lines("day12_input.txt"))
    print(f"Part 2: {answer = }")
