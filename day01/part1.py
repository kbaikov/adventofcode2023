import argparse
from pathlib import Path

import pytest

INPUT_TXT = Path("input.txt")


def compute(s: str) -> int:
    lines = s.splitlines()
    numbers = []
    for line in lines:
        digits = [x for x in line if x.isdigit()]
        numbers.append(int(f"{digits[0]}{digits[-1]}"))

    return sum(numbers)


INPUT_S = """\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""
EXPECTED = 142


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
