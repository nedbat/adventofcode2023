# https://adventofcode.com/2023/day/09

from helpers import *

TEST_INPUT = string_lines(
    """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""
)


def differences(nums):
    for a, b in zip(nums, nums[1:]):
        yield b - a

def next_value(nums, factor=1):
    sequences = [list(nums)]
    while set(sequences[-1]) != {0}:
        sequences.append(list(differences(sequences[-1])))
    sequences.reverse()
    sequences[0].append(0)
    for seq1, seq2 in zip(sequences, sequences[1:]):
        seq2.append(seq1[-1] + factor * seq2[-1])
    return factor * sequences[-1][-1]

def parse_sequences(lines):
    return [list(map(int, line.split())) for line in lines]

def test_next_value():
    seqs = parse_sequences(TEST_INPUT)
    assert [next_value(seq) for seq in seqs] == [18, 28, 68]

def part1(lines):
    seqs = parse_sequences(lines)
    return sum(map(next_value, seqs))


def test_part1():
    assert part1(TEST_INPUT) == 114


if __name__ == "__main__":
    answer = part1(file_lines("day09_input.txt"))
    print(f"Part 1: {answer = }")


def part2(lines):
    seqs = parse_sequences(lines)
    seqs = [list(reversed(seq)) for seq in seqs]
    return sum(next_value(seq, -1) for seq in seqs)


def test_part2():
    assert part2(TEST_INPUT) == 2



if __name__ == "__main__":
    answer = part2(file_lines("day09_input.txt"))
    print(f"Part 2: {answer = }")
