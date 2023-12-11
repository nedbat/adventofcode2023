# https://adventofcode.com/2023/day/11

import itertools

from helpers import *

TEST_INPUT = string_lines(
    """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""
)


def parse_galaxies(lines):
    galaxies = set()
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            if ch == "#":
                galaxies.add((x, y))
    return galaxies


def extent(galaxies):
    return (
        max(x for x, _ in galaxies) + 1,
        max(y for _, y in galaxies) + 1,
    )


def test_extent():
    assert extent(parse_galaxies(TEST_INPUT)) == (10, 10)


def gaps(galaxies):
    maxx, maxy = extent(galaxies)
    xs = set(range(maxx))
    ys = set(range(maxy))
    for gx, gy in galaxies:
        xs.discard(gx)
        ys.discard(gy)
    return xs, ys


def test_gaps():
    assert gaps(parse_galaxies(TEST_INPUT)) == ({2, 5, 8}, {3, 7})

def distance(g1, g2, xgaps, ygaps):
    g1x, g1y = g1
    g2x, g2y = g2
    g1x, g2x = sorted([g1x, g2x])
    g1y, g2y = sorted([g1y, g2y])
    extrax = sum(1 for x in xgaps if g1x < x < g2x)
    extray = sum(1 for y in ygaps if g1y < y < g2y)
    return (g2x - g1x) + extrax + (g2y - g1y) + extray


def part1(lines):
    galaxies = parse_galaxies(lines)
    xgaps, ygaps = gaps(galaxies)
    total = 0
    for g1, g2 in itertools.combinations(galaxies, r=2):
        total += distance(g1, g2, xgaps, ygaps)
    return total


def test_part1():
    assert part1(TEST_INPUT) == 374


if __name__ == "__main__":
    answer = part1(file_lines("day11_input.txt"))
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
#     answer = part2(file_lines("day11_input.txt"))
#     print(f"Part 2: {answer = }")
