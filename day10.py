# https://adventofcode.com/2023/day/10

import itertools
import re
from dataclasses import dataclass

from helpers import *

TEST_INPUT = string_lines(
    """\
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""
)


def parse_pipes(lines):
    pipes = {}
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            if ch == "S":
                start = (x, y)
            elif ch == ".":
                pass
            else:
                pipes[(x, y)] = ch
    return start, pipes


PIPE_DIRECTIONS = [
    ("|", (0, -1), (0, 1)),
    ("-", (1, 0), (-1, 0)),
    ("L", (0, -1), (1, 0)),
    ("J", (0, -1), (-1, 0)),
    ("7", (-1, 0), (0, 1)),
    ("F", (1, 0), (0, 1)),
]

# (ch, in-direction): out-direction
# ('|', (0, -1)): (0, -1)
NEXT_DIRECTIONS = {}
for ch, (dx1, dy1), (dx2, dy2) in PIPE_DIRECTIONS:
    NEXT_DIRECTIONS[(ch, (-dx1, -dy1))] = (dx2, dy2)
    NEXT_DIRECTIONS[(ch, (-dx2, -dy2))] = (dx1, dy1)


def possible_steps(xy, pipes):
    """Find all possible steps away from (start)"""
    x, y = xy
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ch = pipes.get((x + dx, y + dy))
        if ch:
            next_dir = NEXT_DIRECTIONS.get((ch, (dx, dy)))
            if next_dir:
                yield dx, dy

def test_possible_steps():
    assert set(possible_steps(*parse_pipes(TEST_INPUT))) == {(0, 1), (1, 0)}

            
def part1(lines):
    start, pipes = parse_pipes(lines)
    x, y = start
    # print(f"Starting at {start}")
    dx, dy = next(possible_steps(start, pipes))
    x += dx; y += dy
    # print(f"First step: {dx, dy} to {x, y}")
    steps = 1
    while (x, y) != start:
        ch = pipes[x, y]
        dx, dy = NEXT_DIRECTIONS[(ch, (dx, dy))]
        x += dx; y += dy
        # print(f"Pipe {ch} steps {dx, dy} to {x, y}")
        steps += 1
    return steps // 2


def test_part1():
    assert part1(TEST_INPUT) == 8


if __name__ == "__main__":
    answer = part1(file_lines("day10_input.txt"))
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
#     answer = part2(file_lines("day10_input.txt"))
#     print(f"Part 2: {answer = }")
