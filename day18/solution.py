from __future__ import annotations
import itertools
import math
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

    def go(self, direction: str, distance: int) -> Point:
        match direction:
            case "R":
                return Point(self.x + distance, self.y)
            case "L":
                return Point(self.x - distance, self.y)
            case "U":
                return Point(self.x, self.y + distance)
            case "D":
                return Point(self.x, self.y - distance)
            case _:
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

    def follow(self, p: Point) -> Point:
        return p.go(self.direction, self.distance)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.direction} {self.distance} (#{self.color})"


def follow(start: Point, instructions: list[Instruction]) -> Iterable[Point]:
    for instruction in instructions:
        point = instruction.follow(start)
        yield point
        start = point


# This is, apparently, the trapezoid area formula
def area(vertices: list[Point]):
    area = sum(v1.y * v2.x - v1.x * v2.y for v1, v2 in itertools.pairwise(vertices))

    borderLength = sum(
        abs(v1.x - v2.x) + abs(v1.y - v2.y)
        for v1, v2 in itertools.pairwise(vertices + [vertices[0]])
    )

    area = math.ceil((abs(area) + borderLength + 1) / 2)
    return area


def draw(points: list[Point]):
    min_x = min(p.x for p in points)
    max_x = max(p.x for p in points)
    min_y = min(p.y for p in points)
    max_y = max(p.y for p in points)

    for y in range(max_y, min_y - 1, -1):
        for x in range(min_x, max_x + 1):
            p = Point(x, y)
            if p in points:
                print("#", end="")
            else:
                print(" ", end="")
        print()


def main():
    # data = TEST_INPUT.splitlines()
    data = open("input").read().splitlines()

    # part 1
    instructions = [Instruction(line) for line in data]
    vertices = list(follow(Point(0, 0), instructions))
    # print(vertices)
    # draw(vertices)
    ans1 = area(vertices)
    print(ans1)

    # part 2
    instructions2 = [Instruction(line, part2=True) for line in data]
    vertices2 = list(follow(Point(0, 0), instructions2))
    ans2 = area(vertices2)
    print(ans2)


if __name__ == "__main__":
    main()
