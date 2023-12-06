# https://adventofcode.com/2023/day/06

import math


TEST_INPUT = [
    (7, 9),
    (15, 40),
    (30, 200),
]

INPUT = [
    (48, 255),
    (87, 1288),
    (69, 1117),
    (81, 1623),
]


def distance(race_time, button_time):
    return (race_time - button_time) * button_time


def distances(race_time):
    return [distance(race_time, btime) for btime in range(0, race_time + 1)]


def test_distances():
    assert distances(7) == [0, 6, 10, 12, 12, 10, 6, 0]


def ways_to_beat_record(race_time, record):
    return sum(dist > record for dist in distances(race_time))


def test_ways_to_beat_record():
    assert [
        ways_to_beat_record(race_time, record) for race_time, record in TEST_INPUT
    ] == [4, 8, 9]


def part1(times_records):
    return math.prod(
        ways_to_beat_record(race_time, record) for race_time, record in times_records
    )


def test_part1():
    assert part1(TEST_INPUT) == 288


if __name__ == "__main__":
    answer = part1(INPUT)
    print(f"Part 1: {answer = }")


TEST_INPUT2 = [(71530, 940200)]


def test_part2():
    assert part1(TEST_INPUT2) == 71503


INPUT2 = [(48876981, 255128811171623)]

if __name__ == "__main__":
    answer = part1(INPUT2)
    print(f"Part 2: {answer = }")
