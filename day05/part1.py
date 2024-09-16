import argparse
from functools import partial
from pathlib import Path

import pytest

INPUT_TXT = Path("day05/input.txt")


def source_to_destination_list(value: int, destinations: list[range], sources: list[range]) -> int:
    for i, s in enumerate(sources):
        try:
            return destinations[i][s.index(value)]
        except ValueError:
            continue
    return value


seed_soil = partial(
    source_to_destination_list,
    destinations=[range(50, 50 + 2), range(52, 52 + 48)],
    sources=[range(98, 98 + 2), range(50, 50 + 48)],
)

soil_fertilizer = partial(
    source_to_destination_list,
    destinations=[range(0, 37), range(37, 2), range(39, 15)],
    sources=[range(15, 37), range(52, 2), range(0, 15)],
)


def parse_table(s: str) -> dict[str, list[int]]:
    d: dict[str, list[int]] = {}
    for subdict in s.split("\n\n"):
        key, value = subdict.split(":")
        d[key] = value.strip().split("\n")

    for key, value in d.copy().items():
        if len(value) > 1:
            d[key] = [[int(num) for num in string.split()] for string in value]
        else:
            d[key] = [int(num) for num in value[0].split()]
    return d


def list_to_partial(table: list[list[int]]):
    destinations = []
    sources = []
    for entry in table:
        destination_start, source_start, step = entry
        destinations.append(range(destination_start, destination_start + step))
        sources.append(range(source_start, source_start + step))
    return partial(
        source_to_destination_list,
        destinations=destinations,
        sources=sources,
    )


def seed_location(seed_number: int, d_maps):
    d_funcs = {key: list_to_partial(value) for key, value in d_maps.items() if key != "seeds"}

    return d_funcs["humidity-to-location map"](
        d_funcs["temperature-to-humidity map"](
            d_funcs["light-to-temperature map"](
                d_funcs["water-to-light map"](
                    d_funcs["fertilizer-to-water map"](
                        d_funcs["soil-to-fertilizer map"](d_funcs["seed-to-soil map"](seed_number))
                    )
                )
            )
        )
    )


def compute(s: str) -> int:
    d_maps = parse_table(s)

    seed_locations = [seed_location(seed_number, d_maps) for seed_number in d_maps["seeds"]]
    return min(seed_locations)


INPUT_S = """\
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
EXPECTED = 35


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
