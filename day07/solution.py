from dataclasses import dataclass
from enum import Enum
from pprint import pprint

TEST_INPUT = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""

CARD_VALS = "23456789TJQKA"
CARD_VALS_JOKERS = "J23456789TQKA"


class HandType(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7


class Hand:
    def __init__(self, cards_str, bid, joker_rule=False):
        self.joker_rule = joker_rule
        self.cards_str = cards_str
        if joker_rule:
            card_vals = CARD_VALS_JOKERS
        else:
            card_vals = CARD_VALS
        self.cards = [card_vals.index(c) for c in cards_str]
        self.card_set = set(self.cards)
        if joker_rule:
            self.card_set.discard(0)
            self.num_jokers = self.cards.count(0)
        self.card_counts = tuple(sorted(self.cards.count(c) for c in self.card_set))
        self.bid = bid

    def parse(line, joker_rule=False):
        cards_str, bid = line.split()
        return Hand(cards_str, int(bid), joker_rule)

    def __repr__(self) -> str:
        return f"<{self.cards_str}>({self.bid})"

    def type_rank(self):
        if not self.joker_rule or self.num_jokers == 0:
            return {
                (5,): HandType.FIVE_OF_A_KIND,
                (1, 4): HandType.FOUR_OF_A_KIND,
                (2, 3): HandType.FULL_HOUSE,
                (1, 1, 3): HandType.THREE_OF_A_KIND,
                (1, 2, 2): HandType.TWO_PAIR,
                (1, 1, 1, 2): HandType.ONE_PAIR,
                (1, 1, 1, 1, 1): HandType.HIGH_CARD,
            }[self.card_counts]
        elif self.num_jokers == 1:
            return {
                (4,): HandType.FIVE_OF_A_KIND,
                (1, 3): HandType.FOUR_OF_A_KIND,
                (2, 2): HandType.FULL_HOUSE,
                (1, 1, 2): HandType.THREE_OF_A_KIND,
                (1, 1, 1, 1): HandType.ONE_PAIR,
            }[self.card_counts]
        elif self.num_jokers == 2:
            return {
                (3,): HandType.FIVE_OF_A_KIND,
                (1, 2): HandType.FOUR_OF_A_KIND,
                (1, 1, 1): HandType.THREE_OF_A_KIND,
            }[self.card_counts]
        elif self.num_jokers == 3:
            return {
                (2,): HandType.FIVE_OF_A_KIND,
                (1, 1): HandType.FOUR_OF_A_KIND,
            }[self.card_counts]
        elif self.num_jokers == 4:
            return {
                (1,): HandType.FIVE_OF_A_KIND,
            }[self.card_counts]
        elif self.num_jokers == 5:
            return HandType.FIVE_OF_A_KIND
        else:
            raise ValueError(f"Invalid number of jokers: {self.num_jokers}")

    def __lt__(self, other):
        if self.type_rank().value == other.type_rank().value:
            return self.cards < other.cards
        else:
            return self.type_rank().value < other.type_rank().value


def total_winnings(hands):
    hands.sort()
    return sum(h.bid * rank for rank, h in enumerate(hands, 1))


def main():
    with open("input") as f:
        lines = f.readlines()
    # lines = TEST_INPUT.splitlines()
    hands = [Hand.parse(line) for line in lines]
    print(total_winnings(hands))
    hands2 = [Hand.parse(line, joker_rule=True) for line in lines]
    print(total_winnings(hands2))


if __name__ == "__main__":
    main()
