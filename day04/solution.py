from dataclasses import dataclass
from pprint import pprint

TEST_INPUT = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""


class Card:
    def __init__(self, card_number, winning_numbers, have_numbers):
        self.card_number = card_number
        self.winning_numbers = winning_numbers
        self.have_numbers = have_numbers
        self._num_winning = None

    def copies_generated(self):
        return range(self.card_number + 1, self.card_number + 1 + self.num_winning())

    def num_winning(self):
        if self._num_winning == None:
            self._num_winning = sum(
                1 for n in self.have_numbers if n in self.winning_numbers
            )
        return self._num_winning

    def point_value(self):
        match self.num_winning():
            case 0:
                return 0
            case int(n):
                return 2 ** (n - 1)
            case _ as x:
                raise ValueError(f"Unexpected num_winning: {x}")

    def from_line(line: str):
        card_number_part, rest = line.split(": ")
        _, card_number = card_number_part.split()
        winning_numbers_part, have_numbers_part = rest.split("|")
        winning_numbers = Card.parse_numbers(winning_numbers_part)
        have_numbers = Card.parse_numbers(have_numbers_part)
        return Card(
            card_number=int(card_number),
            winning_numbers=winning_numbers,
            have_numbers=have_numbers,
        )

    def parse_numbers(numbers: str):
        return [int(n) for n in numbers.strip().split()]


def part2(cards: list[Card]):
    counts = {n: 1 for n in range(1, len(cards) + 1)}
    for card in cards:
        num_copies = counts[card.card_number]
        for n in card.copies_generated():
            counts[n] += num_copies
    return sum(counts.values())


def main():
    with open("input") as f:
        lines = f.readlines()
    # lines = TEST_INPUT.splitlines()
    cards = [Card.from_line(line) for line in lines]
    # pprint(cards)
    ans1 = sum(card.point_value() for card in cards)
    print(ans1)
    print(part2(cards))


if __name__ == "__main__":
    main()
