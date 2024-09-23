import re
from dataclasses import dataclass
import pathlib

TEST_INPUT = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""


@dataclass
class Card:
    rank: str


ranks = [str(n) for n in range(2, 10)] + list("TJQKA")


def parse_table(text: str):
    cards: list[tuple[str, int]] = []
    for entry in text.splitlines():
        card, bid = entry.split()
        cards.append((card, int(bid)))
    return cards


def calculate_type(card: str) -> int:
    strengh = {
        7: "Five of a kind",
        6: "Four of a kind",
        5: "Full house",
        4: "Three of a kind",
        3: "Two pair",
        2: "One pair",
        1: "High card",
    }
    types = {
        # regexes from https://stackoverflow.com/questions/3463964/regex-to-calculate-straight-poker-hand
        7: re.compile(r"(.)\1{4}.*"),
        6: re.compile(r"(.)\1{3}.*"),
        5: re.compile(r"((.)\2{2}(.)\3{1}|(.)\4{1}(.)\5{2})"),
        4: re.compile(r"(.)\1{2}.*"),
        3: re.compile(r"(.)\1{1}.*(.)\2{1}.*"),
        2: re.compile(r"(.)\1{1}.*"),
    }

    sorted_card = "".join(sorted(card))
    for s, pattern in types.items():
        if pattern.search(sorted_card):
            return s
    return 1


def part1(text: str) -> int:
    cards = parse_table(text)
    # cards.sort(key=itemgetter(1))
    cards_with_rank = []
    for c, bid in cards:
        cards_with_rank.append((c, bid, calculate_type(c)))
    # sort hands according to ranks
    cards_with_rank.sort(key=lambda x: [ranks.index(i) for i in x[0]])

    # sort by calculated type
    cards_with_rank.sort(key=lambda x: (x[2]))

    s = 0
    for i, entry in enumerate(cards_with_rank, start=1):
        s += i * entry[1]

    return s


def test_part1():
    assert part1(TEST_INPUT) == 6440


if __name__ == "__main__":
    # answer = part1(TEST_INPUT)
    answer = part1(pathlib.Path("day07_input.txt").read_text())
    print(answer)


# def part2(text: str)-> int:
#     ...
#
#
# def test_part2():
#     assert part2(TEST_INPUT) == 123456
#
#
#
# if __name__ == "__main__":
#     answer = part2(Path("dayX_input.txt").read_text().splitlines())
#     print(f"Part 2: {answer = }")
