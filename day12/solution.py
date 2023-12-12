from enum import Enum
import itertools
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

    def solve(self) -> Iterable[Checksum]:
        num_unknown = self.states.count(State.UNKNOWN)
        candidates = itertools.product(
            [State.WORKING, State.DAMAGED], repeat=num_unknown
        )
        for candidate in candidates:
            candidate = list(candidate)
            states = self.states.copy()
            for i, c in enumerate(states):
                if c == State.UNKNOWN:
                    states[i] = candidate.pop()
            if checksum(states) == self.checksum:
                yield states

    def num_solutions(self) -> int:
        return sum(1 for _ in self.solve())


def checksum(states: list[State]) -> list[int]:
    assert not any(s == State.UNKNOWN for s in states)
    damaged_groups = (
        list(g) for k, g in itertools.groupby(states) if k == State.DAMAGED
    )
    return [len(g) for g in damaged_groups]


def main():
    lines = TEST_INPUT.splitlines()
    # lines = open("input").readlines()
    records1 = [Record(line) for line in lines]
    ans1 = sum(r.num_solutions() for r in records1)
    print(ans1)
    records2 = [Record(line, unfold=True) for line in lines]
    ans2 = sum(r.num_solutions() for r in records2)
    print(ans2)


if __name__ == "__main__":
    main()
