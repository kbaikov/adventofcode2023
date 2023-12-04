import argparse
from pathlib import Path

import pytest

INPUT_TXT = Path("input.txt")


def get_adjacent_cells(x_coord, y_coord):
    result = {}
    for x, y in [
        (x_coord + i, y_coord + j) for i in (-1, 0, 1) for j in (-1, 0, 1) if i != 0 or j != 0
    ]:
        if (x, y) in grid.cells:
            result[(x, y)] = grid.cells[(x, y)]


def compute(s: str) -> int:
    numbers = s.split(" ")
    for n in numbers:
        pass

    lines = s.splitlines()
    for line in lines:
        pass
    # TODO: implement solution here!
    return 0


INPUT_S = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""
EXPECTED = 4361


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
