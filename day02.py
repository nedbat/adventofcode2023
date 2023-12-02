# https://adventofcode.com/2023/day/2

import re
from dataclasses import dataclass

TEST_INPUT = """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
""".splitlines()


@dataclass
class Cubes:
    red: int = 0
    green: int = 0
    blue: int = 0

    def power(self):
        return self.red * self.green * self.blue


@dataclass
class Game:
    id: int
    handfuls: list[Cubes]


def parse_games(lines):
    for line in lines:
        id = int(re.search(r"Game (\d+):", line)[1])
        handful_texts = line.split(": ")[1].split("; ")
        handfuls = []
        for handful_text in handful_texts:
            cubes = handful_text.split(", ")
            cube_data = sorted(
                (word, int(num)) for cube in cubes for num, word in [cube.split()]
            )
            handfuls.append(Cubes(**dict(cube_data)))
        game = Game(id=id, handfuls=handfuls)
        yield game


def is_possible(handful, bag):
    return (
        handful.red <= bag.red
        and handful.green <= bag.green
        and handful.blue <= bag.blue
    )


def part1(lines):
    bag = Cubes(red=12, green=13, blue=14)
    total = 0
    for game in parse_games(lines):
        if all(is_possible(handful, bag) for handful in game.handfuls):
            total += game.id
    return total


def test_part1():
    assert part1(TEST_INPUT) == 8


if __name__ == "__main__":
    total = part1(open("day02_input.txt"))
    print(f"Part 1: {total = }")


def fewest_cubes(game):
    red = green = blue = 0
    for handful in game.handfuls:
        red = max(red, handful.red)
        green = max(green, handful.green)
        blue = max(blue, handful.blue)
    return Cubes(red, green, blue)


def test_fewest_cubes():
    fewests = [fewest_cubes(game) for game in parse_games(TEST_INPUT)]
    assert fewests == [
        Cubes(red=4, green=2, blue=6),
        Cubes(red=1, green=3, blue=4),
        Cubes(red=20, green=13, blue=6),
        Cubes(red=14, green=3, blue=15),
        Cubes(red=6, green=3, blue=2),
    ]


def part2(lines):
    total = 0
    for game in parse_games(lines):
        total += fewest_cubes(game).power()
    return total


def test_part2():
    assert part2(TEST_INPUT) == 2286


if __name__ == "__main__":
    total = part2(open("day02_input.txt"))
    print(f"Part 2: {total = }")
