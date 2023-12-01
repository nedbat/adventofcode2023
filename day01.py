# https://adventofcode.com/2023/day/1

import re

import pytest

TEST_INPUT = """\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
""".splitlines()


def two_digit_numbers(lines):
    for line in lines:
        digits = re.sub(r"[^0-9]", "", line)
        yield digits[0], digits[-1]


def test_two_digit_numbers():
    assert list(two_digit_numbers(TEST_INPUT)) == [
        ("1", "2"),
        ("3", "8"),
        ("1", "5"),
        ("7", "7"),
    ]


def sum_two_digits(lines):
    total = 0
    for a, b in two_digit_numbers(lines):
        num = int(a + b)
        total += num
    return total


def test_sum_two_digits():
    assert sum_two_digits(TEST_INPUT) == 142


if __name__ == "__main__":
    total = sum_two_digits(open("day01_input.txt"))
    print(f"Part 1: {total = }")

TEST_INPUT2 = """\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
""".splitlines()

DIGITS = "one|two|three|four|five|six|seven|eight|nine"
DIGIT_SUBS = {word: num for num, word in enumerate(DIGITS.split("|"), start=1)}
DIGIT_SUBS.update((d, int(d)) for d in "123456789")


def digit_locations(line):
    for i in range(len(line)):
        for word, num in DIGIT_SUBS.items():
            if line.startswith(word, i):
                yield (i, num)


@pytest.mark.parametrize(
    "line, places",
    [
        ("zoneight234", [(1, 1), (3, 8), (8, 2), (9, 3), (10, 4)]),
        ("xtwone3four", [(1, 2), (3, 1), (6, 3), (7, 4)]),
        ("foooneight", [(3, 1), (5, 8)]),
    ],
)
def test_digit_locations(line, places):
    assert list(digit_locations(line)) == places


def sum_two_digits_part2(lines):
    total = 0
    for line in lines:
        locations = list(digit_locations(line))
        first = locations[0][1]
        last = locations[-1][1]
        total += first * 10 + last
    return total


def test_sum_two_digits_part2():
    assert sum_two_digits_part2(TEST_INPUT2) == 281


if __name__ == "__main__":
    total = sum_two_digits_part2(open("day01_input.txt"))
    print(f"Part 2: {total = }")
