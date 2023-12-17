from __future__ import annotations
from dataclasses import dataclass

TEST_INPUT = """\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""


def turn(direction: str, turn: str) -> str:
    match (direction, turn):
        case ("N", "L"):
            return "W"
        case ("N", "R"):
            return "E"
        case ("S", "L"):
            return "E"
        case ("S", "R"):
            return "W"
        case ("E", "L"):
            return "N"
        case ("E", "R"):
            return "S"
        case ("W", "L"):
            return "S"
        case ("W", "R"):
            return "N"


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def go(self, direction: str) -> Point:
        match direction:
            case "N":
                return Point(self.x, self.y - 1)
            case "S":
                return Point(self.x, self.y + 1)
            case "E":
                return Point(self.x + 1, self.y)
            case "W":
                return Point(self.x - 1, self.y)


class Board:
    def __init__(self, input: str) -> None:
        self.parse(input)

    def parse(self, input: str) -> None:
        self.costs = {}
        for y, line in enumerate(input.splitlines()):
            for x, char in enumerate(line):
                self.costs[Point(x, y)] = int(char)
        self.width = x + 1
        self.height = y + 1

    def in_bounds(self, loc: Point) -> bool:
        return 0 <= loc.x < self.width and 0 <= loc.y < self.height

    def neighbors(self, loc: Point, direction: str, must_turn: bool) -> list[Point]:
        allowed = [turn(direction, "L"), turn(direction, "R")]
        if not must_turn:
            allowed.append(direction)
        locs = (loc.go(d) for d in allowed)
        return [l for l in locs if self.in_bounds(l)]


def main():
    input = TEST_INPUT
    board = Board(input)


if __name__ == "__main__":
    main()
