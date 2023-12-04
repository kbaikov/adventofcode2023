import argparse
import re
from pathlib import Path
from pprint import pprint as print

import pytest

INPUT_TXT = Path("input.txt")


def compute(s: str) -> int:
    lines = s.splitlines()
    max_red = 12
    max_green = 13
    max_blue = 14
    result = 0
    for line in lines:
        red = [int(x) for x in re.findall(r"(\d+) red", line)]
        green = [int(x) for x in re.findall(r"(\d+) green", line)]
        blue = [int(x) for x in re.findall(r"(\d+) blue", line)]
        if (
            all([x <= max_red for x in red])
            and all([x <= max_green for x in green])
            and all([x <= max_blue for x in blue])
        ):
            result += int(re.findall(r"Game (\d+):", line)[0])

    return result


INPUT_S = """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""
EXPECTED = 8


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
