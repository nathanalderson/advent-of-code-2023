from dataclasses import dataclass
from pprint import pprint

TEST_INPUT = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""

CARD_VALS = "23456789TJQKA"


class Hand:
    def __init__(self, cards_str, bid):
        self.cards_str = cards_str
        self.cards = [CARD_VALS.index(c) for c in cards_str]
        self.card_set = set(self.cards)
        self.card_counts = tuple(sorted(self.cards.count(c) for c in self.card_set))
        self.bid = bid

    def parse(line):
        cards_str, bid = line.split()
        return Hand(cards_str, int(bid))

    def __repr__(self) -> str:
        return f"<{self.cards_str}>({self.bid})"

    def type_rank(self):
        return {
            (5,): 7,
            (1, 4): 6,
            (2, 3): 5,
            (1, 1, 3): 4,
            (1, 2, 2): 3,
            (1, 1, 1, 2): 2,
            (1, 1, 1, 1, 1): 1,
        }[self.card_counts]

    def __lt__(self, other):
        if self.type_rank() == other.type_rank():
            return self.cards < other.cards
        else:
            return self.type_rank() < other.type_rank()


def main():
    with open("input") as f:
        lines = f.readlines()
    # lines = TEST_INPUT.splitlines()
    hands = [Hand.parse(line) for line in lines]
    hands.sort()
    # print(hands)
    # print(list(enumerate(hands, 1)))
    ans1 = sum(h.bid * rank for rank, h in enumerate(hands, 1))
    print(ans1)


if __name__ == "__main__":
    main()
