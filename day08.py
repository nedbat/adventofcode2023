# https://adventofcode.com/2023/day/08

import itertools
import re
from dataclasses import dataclass

from helpers import *

TEST_INPUT = string_lines(
    """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""
)


def parse_input(lines):
    it = iter(lines)
    left_right = next(it)
    next(it)
    nodes = {}
    for line in it:
        key, left, right = re.findall(r"\w+", line)
        nodes[key] = (left, right)
    return left_right, nodes


def part1(lines):
    left_right, nodes = parse_input(lines)
    node = "AAA"
    for steps, lr in enumerate(itertools.cycle(left_right), start=1):
        node = nodes[node][lr == "R"]
        if node == "ZZZ":
            break
    return steps

def test_part1():
    assert part1(TEST_INPUT) == 6


if __name__ == "__main__":
    answer = part1(file_lines("day08_input.txt"))
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
#     answer = part2(file_lines("day08_input.txt"))
#     print(f"Part 2: {answer = }")
