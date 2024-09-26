"""based on https://github.com/nedbat/adventofcode2023/blob/main/new.py"""

import pathlib
from typing import Any, Generator, Sequence

TEST_INPUT = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""

FILE = pathlib.Path("day09_input.txt").read_text()


def parse_table(text: str) -> Generator[tuple[int, ...], Any, Any]:
    for line in text.splitlines():
        yield tuple(int(x) for x in line.split())


def extrapolate(sequence: Sequence[int]) -> int:
    s = sequence[:]
    s = [y - x for x, y in zip(s, s[1:])]
    if len(set(s)) == 1:
        return sequence[-1] + s[0]
    else:
        return sequence[-1] + extrapolate(s)


def part1(text: str) -> int:
    table = list(parse_table(text))

    return sum(extrapolate(x) for x in table)


def test_part1():
    assert part1(TEST_INPUT) == 114


def test_extrapolate():
    assert extrapolate([0, 3, 6, 9, 12, 15]) == 18
    assert extrapolate([1, 3, 6, 10, 15, 21]) == 28


if __name__ == "__main__":
    answer = part1(FILE)
    # answer = part1(TEST_INPUT)
    # print(answer)


def extrapolate_backwards(sequence: Sequence[int]) -> int:
    s = sequence[:]
    s = [y - x for x, y in zip(s, s[1:])]
    if len(set(s)) == 1:
        return sequence[0] - s[0]
    else:
        return sequence[0] - extrapolate_backwards(s)


def test_extrapolate_backwards():
    assert extrapolate_backwards([0, 3, 6, 9, 12, 15]) == -3
    assert extrapolate_backwards([1, 3, 6, 10, 15, 21]) == 0
    assert extrapolate_backwards([10, 13, 16, 21, 30, 45]) == 5


def part2(text: str) -> int:
    table = list(parse_table(text))

    return sum(extrapolate_backwards(x) for x in table)


def test_part2():
    assert part2(TEST_INPUT) == 2


if __name__ == "__main__":
    answer = part2(FILE)
    # answer = part2(TEST_INPUT)
    print(answer)
