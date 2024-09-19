"""based on https://github.com/nedbat/adventofcode2023/blob/main/new.py"""

import math
import pathlib
from dataclasses import dataclass

TEST_INPUT = """\
Time:      7  15   30
Distance:  9  40  200
"""


@dataclass
class Race:
    time: int
    distance: int
    ways_to_win: int = 0

    def populate_best_times(self):
        for x in range(self.time):
            d = (self.time - x) * x
            if d > self.distance:
                self.ways_to_win += 1


def parse_table(text):
    records = []
    for line in text.splitlines():
        _, _, t = line.partition(":")
        records.append([int(x) for x in t.split()])
    races = [Race(t, d) for t, d in zip(records[0], records[1])]
    [r.populate_best_times() for r in races]
    return races


def part1(text) -> int:
    races = parse_table(text)
    return math.prod(r.ways_to_win for r in races)


def test_part1():
    assert part1(TEST_INPUT) == 288


if __name__ == "__main__":
    answer = part1(pathlib.Path("day06_input.txt").read_text())
    # print(f"Part 1: {answer = }")
    # print(answer)


def parse_table_part2(text):
    records = []
    for line in text.splitlines():
        _, _, t = line.partition(":")
        records.append(t.split())
    r = Race(int("".join(records[0])), int("".join(records[1])))
    r.populate_best_times()
    return r


def part2(text: str) -> int:
    race = parse_table_part2(text)
    return race.ways_to_win


def test_part2():
    assert part2(TEST_INPUT) == 71503


if __name__ == "__main__":
    answer = part2(pathlib.Path("day06_input.txt").read_text())
    # print(f"Part 2: {answer = }")
    print(answer)
