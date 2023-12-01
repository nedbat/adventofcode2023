# https://adventofcode.com/2023/day/1

import re

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


