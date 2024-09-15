"""taken from https://github.com/nedbat/adventofcode2023/blob/main/day03.py
and https://www.giulianopertile.com/blog/the-definitive-guide-to-graph-problems/"""

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


INPUT_TXT = Path("day03/input.txt")


DOT = "."
NUMBERS = "0123456789"


@dataclass
class Number:
    x: int
    y: int
    ndigits: int
    num: int

    def neighboring_locations(self):
        x0 = self.x - 1
        x1 = self.x + self.ndigits
        return {
            *[(xx, self.y - 1) for xx in range(x0, x1 + 1)],
            (x0, self.y),
            (x1, self.y),
            *[(xx, self.y + 1) for xx in range(x0, x1 + 1)],
        }


def test_neighboring_locations():
    assert Number(3, 4, 3, 123).neighboring_locations() == {
        (2, 3),
        (3, 3),
        (4, 3),
        (5, 3),
        (6, 3),
        (2, 4),
        (6, 4),
        (2, 5),
        (3, 5),
        (4, 5),
        (5, 5),
        (6, 5),
    }


def find_numbers(lines):
    for lineno, line in enumerate(lines):
        for match in re.finditer(r"\d+", line):
            yield Number(match.start(), lineno, len(match[0]), int(match[0]))


def find_symbols(lines):
    for lineno, line in enumerate(lines):
        for match in re.finditer(r"[^.\d\s]", line):
            yield (match.start(), lineno, match[0])


def number_count(grid: list[str]) -> int:
    visited = set()
    numbers = []
    buffer = {}
    # With this nested for loop, we iterate through our grid
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            # We continue if the cell is a dot
            if grid[row][col] == DOT:
                continue
            # we also continue if the cell has been visited
            if (row, col) in visited:
                continue
            # If we reach this line, it means that we found a number,
            # our next step is to keep exploring this number,
            # and mark of its adjancent cells as visited, so we can
            # skip them in the next iteration of the foor loop
            if valid_number := parse_number(grid, row, col, visited):
                numbers.append(valid_number)

    return sum(numbers)


def parse_number(grid, row, col, visited):
    parsed_number = ""
    queue = [(row, col)]
    while len(queue) > 0:
        row, col = queue.pop(0)
        # We check if the node has been visited,
        # if so we skip it.
        if (row, col) in visited:
            continue
        # We mark the node as visited, and check if
        # the current node is a dot, if so we skip it.
        visited.add((row, col))
        if grid[row][col] == DOT:
            continue
        if grid[row][col] not in NUMBERS:
            continue
        parsed_number += grid[row][col]
        # We get the neighboring nodes of
        # the current node, and then add them to the queue.
        neighbors = get_neigbors(grid, row, col)
        for neighbor in neighbors:
            queue.append(neighbor)
    return int(parsed_number) if parsed_number else None


def get_neigbors(grid: list[str], row: int, col: int) -> list[tuple[int, int]]:
    # We get the nodes around the current node.
    neighbors = []
    # Up
    if row - 1 >= 0:
        neighbors.append((row - 1, col))
    # Down
    if row + 1 < len(grid):
        neighbors.append((row + 1, col))
    # Left
    if col - 1 >= 0:
        neighbors.append((row, col - 1))
    # Right
    if col + 1 < len(grid[0]):
        neighbors.append((row, col + 1))

    return neighbors


def compute(s: str) -> int:
    grid = s.splitlines()
    return number_count(grid)


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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file, encoding="utf-8") as f:
        print(compute(f.read()))

    return 0


def part1(lines):
    numbers = list(find_numbers(lines))
    symbols = list(find_symbols(lines))
    symbol_spots = {(x, y) for x, y, s in symbols}
    part_numbers = []
    for num in numbers:
        if num.neighboring_locations() & symbol_spots:
            part_numbers.append(num)
    return sum(pnum.num for pnum in part_numbers)


def gears(lines):
    """from https://github.com/nedbat/adventofcode2023/blob/main/day03.py"""
    numbers = list(find_numbers(lines))
    stars = [(x, y) for x, y, s in find_symbols(lines) if s == "*"]
    for star in stars:
        adjacent_nums = []
        possible_rows = {star[1] - 1, star[1], star[1] + 1}
        for num in numbers:
            if num.y not in possible_rows:
                continue
            if star in num.neighboring_locations():
                adjacent_nums.append(num)
        if len(adjacent_nums) == 2:
            yield tuple(anum.num for anum in adjacent_nums)


def test_gears():
    assert list(gears(INPUT_S.splitlines())) == [(467, 35), (755, 598)]


def part2(lines):
    return sum(g1 * g2 for g1, g2 in gears(lines))


if __name__ == "__main__":
    # raise SystemExit(main())
    print(part2(INPUT_TXT.read_text().splitlines()))
    # print(part2(INPUT_S.splitlines()))
