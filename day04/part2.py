import argparse
from dataclasses import dataclass
from pathlib import Path
from pprint import pprint as print

import pytest

INPUT_TXT = Path("input.txt")


@dataclass
class Card:
    your_numbers: list[int]
    winning_numbers: list[int]
    amount: int = 1


def parse_cards(s: str) -> list[Card]:
    cards: list[Card] = []
    for line in s.splitlines():
        you_have, winning = line.split(":")[1].split("|")
        you_have = [int(x) for x in you_have.split()]
        winning = [int(x) for x in winning.split()]
        cards.append(Card(amount=1, your_numbers=you_have, winning_numbers=winning))

    return cards


def process_card(c: Card) -> int:
    score = 0
    for number in c.your_numbers:
        if number in c.winning_numbers:
            score += 1
    return score


def compute(s: str) -> int:
    cards = parse_cards(s)
    for card_number, card in enumerate(cards):
        win_amount = process_card(card)
        for _ in range(card.amount):
            for x in range(1, win_amount + 1):
                cards[card_number + x].amount += 1

    return sum(c.amount for c in cards)


INPUT_S = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""
EXPECTED = 30


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
