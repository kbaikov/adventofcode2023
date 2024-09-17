"""based on https://github.com/norvig/pytudes/blob/main/ipynb/Advent-2023.ipynb"""

from dataclasses import dataclass
from itertools import batched
from pathlib import Path
from typing import Collection

INPUT_TXT = Path("day05/input.txt")

TEST_INPUT = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""


@dataclass
class Mapping:
    range: range
    offset: int


def parse_almanac(paragraph) -> tuple:
    """Parse a paragraph which can be either a list of seeds or a map."""
    if paragraph.startswith("seeds:"):
        name, *seed_numbers = paragraph.split()
        return ("seeds", [int(seed) for seed in seed_numbers])
    else:
        name, *mappings = paragraph.splitlines()
        int_mappings = [
            list(map(int, entry)) for entry in [mapping.split() for mapping in mappings]
        ]
        final_mappings = []
        for entry in int_mappings:
            dest, src, length = entry
            final_mappings.append(Mapping(range(src, src + length), dest - src))

        return (name, final_mappings)


def parse_input(text):
    paragraphs = text.split("\n\n")
    return map(parse_almanac, paragraphs)


def first(iterable, default=None) -> object | None:
    """The first element in an iterable, or the default if iterable is empty."""
    return next(iter(iterable), default)


def convert(number: int, mappings: list[Mapping]) -> int:
    """Convert number if it is contained in one of the range mappings; else leave unchanged."""
    return first(number + m.offset for m in mappings if number in m.range) or number


def multi_convert(number: int, almanac):
    """Convert number using successive range mappings in almanac (but not 'seeds')."""
    for name, mappings in almanac:
        if name != "seeds":
            number = convert(number, mappings)
    return number


def lowest_location(almanac):
    """What is the lowest location number that corresponds to one of the seed numbers in almanac?"""
    name, seeds = almanac[0]
    return min(multi_convert(seed, almanac) for seed in seeds)


def part2(text):
    almanac = list(parse_input(text))
    return lowest_location_with_ranges(almanac)


def convert_ranges(ranges: Collection[range], mappings: list[Mapping]) -> set[range]:
    """Convert a set of ranges into another set of ranges, as specified by the mappings."""
    ranges = set(ranges)  # Make `ranges` be a set if it is not already
    result = set()  # This will be the output set of ranges
    while ranges:
        r = ranges.pop()
        m = find_intersecting_mapping(r, mappings)
        if m:
            start, stop = max(r.start, m.range.start), min(r.stop, m.range.stop)
            result.add(range(start + m.offset, stop + m.offset))
            if r.start < start:
                ranges.add(range(r.start, start))
            if stop < r.stop:
                ranges.add(range(stop, r.stop))
        else:
            result.add(r)
    return result


def multi_convert_ranges(ranges: Collection[range], almanac):
    """Convert ranges using all the range mappings in almanac (except 'seeds') successively."""
    num_seeds = sum(map(len, ranges))
    for name, mappings in almanac:
        if name != "seeds":
            ranges = list(convert_ranges(ranges, mappings))
            assert (
                sum(map(len, ranges)) == num_seeds
            ), f"was {num_seeds} seeds; now {sum(map(len, ranges))}"
    return ranges


def lowest_location_with_ranges(almanac):
    """What is the lowest location number that corresponds to one of the seed numbers in almanac?"""
    name, pairs = almanac[0]
    ranges = {range(start, start + length) for (start, length) in batched(pairs, 2)}
    converted_ranges = multi_convert_ranges(ranges, almanac)
    return min(r.start for r in converted_ranges)


def find_intersecting_mapping(r: range, mappings) -> Mapping | None:
    """If there is a mapping that intersects with range r, return it."""
    return first(m for m in mappings if (m.range.start in r) or (r.start in m.range))


test_maps = [Mapping(range(15, 5), offset=2), Mapping(range(5, 10), offset=100)]
assert find_intersecting_mapping(range(1, 10), test_maps) == Mapping(range(5, 10), offset=100)
assert set(convert_ranges({range(1, 10)}, test_maps)) == {range(1, 5), range(105, 110)}


def test_part2():
    assert part2(TEST_INPUT) == 46


if __name__ == "__main__":
    answer = part2(INPUT_TXT.read_text())
    print(f"Part 2: {answer = }")
