from __future__ import annotations
from dataclasses import dataclass, field
import functools
from pprint import pprint
import string
from typing import Iterable

TEST_INPUT = """\
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
"""


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"


@dataclass()
class Brick:
    label: str
    p1: Point
    p2: Point
    supports: list[Brick] = field(default_factory=list)
    supported_by: list[Brick] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"<{self.p1} ~ {self.p2}> {self.label}"

    @functools.cached_property
    def columns(self) -> set[tuple[int, int]]:
        return set(
            (x, y)
            for x in range(self.p1.x, self.p2.x + 1)
            for y in range(self.p1.y, self.p2.y + 1)
        )

    def drop_to(self, floor: int) -> None:
        assert floor < self.min_z()
        drop_by = self.min_z() - floor - 1
        assert drop_by >= 0
        self.p1 = Point(self.p1.x, self.p1.y, self.p1.z - drop_by)
        self.p2 = Point(self.p2.x, self.p2.y, self.p2.z - drop_by)

    def min_z(self) -> int:
        return min(self.p1.z, self.p2.z)

    def max_z(self) -> int:
        return min(self.p1.z, self.p2.z)


class Tower:
    def __init__(self, bricks: list[Brick]) -> None:
        self.bricks = sorted(bricks, key=lambda b: b.min_z())
        self.length = max(b.p2.x for b in bricks) + 1
        self.width = max(b.p2.y for b in bricks) + 1

    def __repr__(self) -> str:
        return f"<Tower: {self.bricks}>"

    def settle(self) -> None:
        highest_by_column: dict[tuple[int, int], int] = {
            (x, y): 0 for x in range(self.length) for y in range(self.width + 1)
        }
        for brick in self.bricks:
            floor = 0
            for column in brick.columns:
                floor = max(floor, highest_by_column[column])
            assert floor < brick.min_z()
            brick.drop_to(floor)
            for column in brick.columns:
                highest_by_column[column] = brick.max_z()

    def calculate_supports(self):
        for brick in self.bricks:
            for other_brick in self.bricks:
                if brick is other_brick:
                    continue
                if (
                    brick.columns & other_brick.columns
                    and brick.max_z() + 1 == other_brick.min_z()
                ):
                    brick.supports.append(other_brick)
                    other_brick.supported_by.append(brick)

    def part1(self) -> Iterable[Brick]:
        for brick in self.bricks:
            if all(len(other_brick.supported_by) > 1 for other_brick in brick.supports):
                yield brick


def parse(line: str, label: str) -> Brick:
    p1, p2 = line.split("~")
    x1, y1, z1 = map(int, p1.split(","))
    x2, y2, z2 = map(int, p2.split(","))
    return Brick(label, Point(x1, y1, z1), Point(x2, y2, z2))


def main():
    # data = TEST_INPUT.splitlines()
    data = open("input").read().splitlines()
    bricks = [parse(line, str(i)) for i, line in enumerate(data)]
    tower = Tower(bricks)
    print("settling...")
    pprint(tower.bricks)
    tower.settle()
    print("calculating supports...")
    tower.calculate_supports()
    print("calculating disintegrations...")
    can_disintegrate = list(tower.part1())
    print("done.")
    pprint(len(can_disintegrate))
    # Wrong: 509


if __name__ == "__main__":
    main()
