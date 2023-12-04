import argparse
from pathlib import Path

import pytest

INPUT_TXT = Path("input.txt")

WORD_TO_DIGIT = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def compute(s: str) -> int:
    """from https://github.com/jonathanpaulson/AdventOfCode/blob/master/2023/1.py"""
    lines = s.splitlines()
    numbers = []
    for line in lines:
        digits_line = []
        for i, char in enumerate(line):
            if char.isdigit():
                digits_line.append(char)
            for word, number in WORD_TO_DIGIT.items():
                if line[i:].startswith(word):
                    digits_line.append(number)
        numbers.append(int(f"{digits_line[0]}{digits_line[-1]}"))
    return sum(numbers)


INPUT_S = """\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""
EXPECTED = 281


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file, encoding="utf-8") as f:
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
