from __future__ import annotations
import itertools
import re
from dataclasses import dataclass
from typing import Iterable


TEST_INPUT = """\
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def go(self, direction: str, distance: int) -> list[Point]:
        if direction == "R":
            return [Point(x + 1, self.y) for x in range(self.x, self.x + distance)]
        elif direction == "L":
            return [Point(x - 1, self.y) for x in range(self.x, self.x - distance, -1)]
        elif direction == "U":
            return [Point(self.x, y + 1) for y in range(self.y, self.y + distance)]
        elif direction == "D":
            return [Point(self.x, y - 1) for y in range(self.y, self.y - distance, -1)]
        else:
            raise ValueError(f"Invalid direction: {direction}")


class Instruction:
    def __init__(self, line: str, part2: bool = False):
        m = re.match(r"([RULD]) (\d+) \(#([0-9a-f]{6})\)", line)
        if m and not part2:
            self.direction, distance_str, self.color = m.groups()
            self.distance = int(distance_str)
        elif m and part2:
            _, _, self.color = m.groups()
            dist_str = self.color[:5]
            self.distance = int(dist_str, 16)
            match self.color[5]:
                case "0":
                    self.direction = "R"
                case "1":
                    self.direction = "D"
                case "2":
                    self.direction = "L"
                case "3":
                    self.direction = "U"
        else:
            raise ValueError(f"Invalid instruction: {line}")

    def follow(self, p: Point) -> list[Point]:
        return p.go(self.direction, self.distance)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.direction} {self.distance} (#{self.color})"


def follow(start: Point, instructions: list[Instruction]) -> Iterable[Point]:
    yield start
    for instruction in instructions:
        points = instruction.follow(start)
        yield from points
        start = points[-1]


def fill(border: set[Point], start: Point) -> set[Point]:
    interior = set()
    queue = [start]
    while queue:
        p = queue.pop()
        if p in border or p in interior:
            continue
        interior.add(p)
        queue.extend(
            itertools.chain.from_iterable(p.go(direction, 1) for direction in "RULD")
        )
    return interior


def draw(points: set[Point], interior: set[Point]):
    min_x = min(p.x for p in points)
    max_x = max(p.x for p in points)
    min_y = min(p.y for p in points)
    max_y = max(p.y for p in points)

    for y in range(max_y, min_y - 1, -1):
        for x in range(min_x, max_x + 1):
            p = Point(x, y)
            if p in points:
                print("#", end="")
            elif p in interior:
                print(".", end="")
            else:
                print(" ", end="")
        print()


def main():
    # data = TEST_INPUT.splitlines()
    data = open("input").read().splitlines()

    # part 1
    instructions = [Instruction(line) for line in data]
    border = set(follow(Point(0, 0), instructions))
    # interior_point = Point(1, -1)  # TEST - Found by inspection
    interior_point = Point(60, 1)  # Found by inspection
    interior = fill(border, interior_point)
    print(border)
    draw(border, interior)
    print(len(interior) + len(border))

    # part 2
    instructions2 = [Instruction(line, part2=True) for line in data]
    border2 = set(follow(Point(0, 0), instructions2))
    interior_point2 = Point(60, 1)  # ???
    interior2 = fill(border2, interior_point2)
    print(len(interior2) + len(border2))


if __name__ == "__main__":
    main()
