from enum import Enum
import itertools
from pprint import pprint
from typing import Iterable


TEST_INPUT = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""

Checksum = list[int]


class State(Enum):
    UNKNOWN = 0
    WORKING = 1
    DAMAGED = 2

    def from_char(c):
        if c == "?":
            return State.UNKNOWN
        elif c == ".":
            return State.WORKING
        elif c == "#":
            return State.DAMAGED
        else:
            raise ValueError(f"Invalid state character: {c}")

    def __str__(self) -> str:
        match self:
            case State.UNKNOWN:
                return "?"
            case State.WORKING:
                return "."
            case State.DAMAGED:
                return "#"

    def __repr__(self) -> str:
        return str(self)


class Record:
    def __init__(self, line, unfold=False) -> None:
        state_part, checksum_part = line.split()
        self.states = self.parse_state(state_part)
        self.checksum = self.parse_checksum(checksum_part)
        if unfold:
            self.states = [*self.states, State.UNKNOWN] * 5
            self.checksum = self.checksum * 5

    def parse_state(self, part):
        return [State.from_char(c) for c in part]

    def parse_checksum(self, part):
        return [int(c) for c in part.split(",")]

    def __repr__(self) -> str:
        states = "".join(str(s) for s in self.states)
        return f"<{states}>{self.checksum}"

    def check(states: list[State], checksum: Checksum) -> bool:
        return checksum == checksum(states)

    def solve(self, states: tuple[State], checksum: tuple[int], acc: int) -> int:
        if len(states) == 0 and len(checksum) == 0:
            return acc + 1
        elif len(states) == 0 or len(checksum) == 0:
            return acc
        elif len(states) < checksum[0]:
            return acc
        elif any(s == State.WORKING for s in states[: checksum[0]]):
            return acc
        else:
            head, *rest = states
            if head == State.WORKING:
                return self.solve(rest, checksum, acc)
            if head == State.UNKNOWN:
                return self.solve((State.WORKING, *rest), checksum, acc) + self.solve(
                    (State.DAMAGED, *rest), checksum, acc
                )
            else:  # state == State.DAMAGED
                return self.solve(states[: checksum[0]], checksum[1:], acc)

    def num_solutions(self) -> int:
        return self.solve(tuple(self.states), tuple(self.checksum), 0)


def checksum(states: list[State]) -> list[int]:
    damaged_groups = (
        list(g) for k, g in itertools.groupby(states) if k == State.DAMAGED
    )
    return [len(g) for g in damaged_groups]


def main():
    lines = TEST_INPUT.splitlines()
    lines = open("input").readlines()
    records1 = [Record(line) for line in lines]
    ans1 = sum(r.num_solutions() for r in records1)
    print(ans1)
    # records2 = [Record(line, unfold=True) for line in lines]
    # r = records2[1]
    # print(r.num_solutions())
    # ans2 = sum(r.num_solutions() for r in records2)
    # print(ans2)


if __name__ == "__main__":
    main()
