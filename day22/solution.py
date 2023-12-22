from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass, field, replace
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
    supports: list[str] = field(default_factory=list)
    supported_by: list[str] = field(default_factory=list)

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
        return max(self.p1.z, self.p2.z)

    def copy(self) -> Brick:
        return Brick(
            self.label, self.p1, self.p2, self.supports[:], self.supported_by[:]
        )

    def __hash__(self) -> Point:
        return self.p1

    def __eq__(self, other: object) -> bool:
        return type(other) == Brick and self.label == other.label


class Tower:
    def __init__(self, bricks: list[Brick]) -> None:
        self.bricks = sorted(bricks, key=lambda brick: brick.min_z())
        self.bricks_by_label = {brick.label: brick for brick in self.bricks}

    def __repr__(self) -> str:
        return f"<Tower: {self.bricks}>"

    def settle(self) -> None:
        highest_by_column: dict[tuple[int, int], int] = defaultdict(lambda: 0)
        for brick in self.bricks:
            floor = 0
            for column in brick.columns:
                floor = max(floor, highest_by_column[column])
            assert floor < brick.min_z()
            brick.drop_to(floor)
            for column in brick.columns:
                highest_by_column[column] = brick.max_z()
        self.bricks.sort(key=lambda brick: brick.min_z())

    def calculate_supports(self):
        for brick in self.bricks:
            for other_brick in self.bricks:
                if brick is other_brick:
                    continue
                if (
                    brick.max_z() + 1 == other_brick.min_z()
                    and brick.columns & other_brick.columns
                ):
                    brick.supports.append(other_brick.label)
                    other_brick.supported_by.append(brick.label)

    def remove(self, brick: Brick) -> None:
        for other_brick_label in brick.supports:
            other_brick = self.bricks_by_label[other_brick_label]
            other_brick.supported_by.remove(brick.label)
        self.bricks.remove(brick)
        self.bricks_by_label.pop(brick.label)

    def part1(self) -> Iterable[Brick]:
        for brick in self.bricks:
            if all(
                len(self.bricks_by_label[other_brick_label].supported_by) > 1
                for other_brick_label in brick.supports
            ):
                yield brick

    def copy(self) -> Tower:
        return Tower([brick.copy() for brick in self.bricks])


def num_fall_if_removed(brick_in: str, tower: Tower) -> int:
    tower = tower.copy()
    sum = 0
    to_remove = [tower.bricks_by_label[brick_in]]
    while to_remove:
        brick_to_remove = to_remove.pop(0)
        tower.remove(brick_to_remove)
        for b in tower.bricks:
            if len(b.supported_by) == 0 and b.min_z() != 1 and b not in to_remove:
                sum += 1
                to_remove.append(b)
    return sum


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
    tower.settle()
    print("calculating supports...")
    tower.calculate_supports()
    print("calculating disintegrations...")
    can_disintegrate = list(tower.part1())
    print("done.")
    pprint(len(can_disintegrate))

    ans2 = sum(num_fall_if_removed(brick.label, tower) for brick in tower.bricks)
    print(ans2)


if __name__ == "__main__":
    main()
