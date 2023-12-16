from enum import Enum
import functools
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
            self.states = [
                *self.states,
                State.UNKNOWN,
                *self.states,
                State.UNKNOWN,
                *self.states,
                State.UNKNOWN,
                *self.states,
                State.UNKNOWN,
                *self.states,
            ]
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

    def num_solutions(self) -> int:
        solve.cache_clear()
        return solve(tuple(self.states), tuple(self.checksum))


def checksum(states: list[State]) -> list[int]:
    damaged_groups = (
        list(g) for k, g in itertools.groupby(states) if k == State.DAMAGED
    )
    return [len(g) for g in damaged_groups]


def counts(states: list[State]) -> (int, int, int):
    working = 0
    damaged = 0
    unknown = 0
    for s in states:
        if s == State.WORKING:
            working += 1
        elif s == State.DAMAGED:
            damaged += 1
        else:
            unknown += 1
    return (working, damaged, unknown)


@functools.cache
def solve(states: tuple[State], checksum: tuple[int]) -> int:
    _num_working, num_damaged, num_unknown = counts(states)
    if num_damaged == 0 and len(checksum) == 0:
        return 1
    elif len(states) == 0 or len(checksum) == 0:
        return 0
    elif num_damaged + num_unknown < sum(checksum):
        return 0
    else:
        head, *rest = states
        if head == State.WORKING:
            return solve(tuple(rest), checksum)
        elif head == State.UNKNOWN:
            return solve((State.DAMAGED, *rest), checksum) + solve(
                (State.WORKING, *rest), checksum
            )
        else:  # state == State.DAMAGED
            c = checksum[0]
            if len(states) < c:
                return 0
            elif any(s == State.WORKING for s in states[:c]):
                return 0
            elif c == len(states) or states[c] != State.DAMAGED:
                return solve(states[c + 1 :], checksum[1:])
            else:
                return 0


def main():
    # lines = TEST_INPUT.splitlines()
    lines = open("input").readlines()
    records1 = [Record(line) for line in lines]
    num_solutions = [r.num_solutions() for r in records1]
    # pprint(num_solutions)
    ans1 = sum(num_solutions)
    print(ans1)
    records2 = [Record(line, unfold=True) for line in lines]
    num_solutions2 = [r.num_solutions() for r in records2]
    # pprint(num_solutions2)
    ans2 = sum(num_solutions2)
    print(ans2)
    # 690697471078056 -- too high


if __name__ == "__main__":
    main()
