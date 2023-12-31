from __future__ import annotations
from dataclasses import dataclass
import functools
from pprint import pprint
from typing import Iterable


TEST_INPUT = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def go(self, dir: str) -> Point:
        match dir:
            case "n":
                return Point(self.x, self.y - 1)
            case "s":
                return Point(self.x, self.y + 1)
            case "e":
                return Point(self.x + 1, self.y)
            case "w":
                return Point(self.x - 1, self.y)


class Tile:
    def __init__(self, c: str) -> None:
        self.c = c

    def outs(self, dir: str) -> [str]:
        match self.c:
            case "|" if dir in "ns":
                return [dir]
            case "|" if dir in "ew":
                return ["n", "s"]
            case "-" if dir in "ew":
                return [dir]
            case "-" if dir in "ns":
                return ["e", "w"]
            case "\\" if dir == "n":
                return ["w"]
            case "\\" if dir == "s":
                return ["e"]
            case "\\" if dir == "e":
                return ["s"]
            case "\\" if dir == "w":
                return ["n"]
            case "/" if dir == "n":
                return ["e"]
            case "/" if dir == "s":
                return ["w"]
            case "/" if dir == "e":
                return ["n"]
            case "/" if dir == "w":
                return ["s"]

    def __str__(self) -> str:
        return self.c

    def __repr__(self) -> str:
        return str(self)


class Board:
    def __init__(self, input: str) -> None:
        self.parse_input(input)

    def parse_input(self, input: str) -> None:
        self.tiles = {}
        for y, line in enumerate(input.splitlines()):
            for x, c in enumerate(line):
                if c != ".":
                    self.tiles[Point(x, y)] = Tile(c)
        self.width = x + 1
        self.height = y + 1

    def in_bounds(self, point: Point) -> bool:
        return 0 <= point.x < self.width and 0 <= point.y < self.height

    def follow(self, point: Point, dir: str) -> Iterable[Point]:
        explored: set((Point, str)) = set()
        to_explore = [(point, dir)]
        while to_explore:
            point, dir = to_explore.pop()
            if (point, dir) in explored:
                continue
            yield point
            explored.add((point, dir))
            if tile := self.tiles.get(point):
                for p, d in ((point.go(d), d) for d in tile.outs(dir)):
                    if self.in_bounds(p):
                        to_explore.append((p, d))
            else:
                if self.in_bounds(p := point.go(dir)):
                    to_explore.append((p, dir))

    def num_energized(self, point: Point, dir: str) -> int:
        count = len(set(self.follow(point, dir)))
        return count

    def part2(self) -> int:
        starting_pointdirs = [
            *[(Point(0, y), "e") for y in range(self.height)],
            *[(Point(x, 0), "s") for x in range(self.width)],
            *[(Point(x, self.height - 1), "n") for x in range(self.width)],
            *[(Point(self.width - 1, y), "w") for y in range(self.height)],
        ]
        return max(self.num_energized(point, dir) for point, dir in starting_pointdirs)

    def __str__(self) -> str:
        return "\n".join(
            "".join(str(self.tiles.get(Point(x, y), ".")) for x in range(self.width))
            for y in range(self.height)
        )


def main():
    # input = TEST_INPUT.strip()
    input = open("input").read()
    board = Board(input.strip())
    ans1 = board.num_energized(Point(0, 0), "e")
    pprint(ans1)
    pprint(board.part2())


if __name__ == "__main__":
    main()
