from __future__ import annotations
import math
from pprint import pprint
from dataclasses import dataclass
from typing import Iterable

TEST_INPUT = """\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def reflect(self, x: float | None, y: float | None) -> Point:
        offset_x = self.x - x if x else 0
        offset_y = self.y - y if y else 0
        return Point(self.x - (offset_x * 2), self.y - (offset_y * 2))


Board = set[Point]


class Board:
    def __init__(self, board_str: str) -> None:
        self.locs = set(Board.parse(board_str))
        lines = board_str.splitlines()
        self.height = len(lines)
        self.width = len(lines[0])

    def parse(board_str: str) -> Iterable[Point]:
        for y, line in enumerate(board_str.splitlines()):
            for x, char in enumerate(line):
                if char == "#":
                    yield Point(x, y)

    def is_reflected(self, axis: float, direction: str) -> bool:
        for point in self.locs:
            match direction:
                case "x":
                    reflected = point.reflect(axis, None)
                case "y":
                    reflected = point.reflect(None, axis)
            if (
                0 <= reflected.x < self.width and 0 <= reflected.y < self.height
            ) and reflected not in self.locs:
                return False
        return True

    def find_reflection_point(self) -> (float, str):
        for x in range(self.width - 1):
            axis = x + 0.5
            if self.is_reflected(axis, "x"):
                return axis, "x"
        for y in range(self.height - 1):
            axis = y + 0.5
            if self.is_reflected(axis, "y"):
                return axis, "y"
        raise ValueError("No reflection point found")

    def get_reflection_score(self) -> int:
        axis, direction = self.find_reflection_point()
        cols_before = math.ceil(axis)
        if direction == "x":
            return cols_before
        elif direction == "y":
            return cols_before * 100
        else:
            raise ValueError(f"Invalid direction: {direction}")


def main():
    data = TEST_INPUT
    data = open("input").read()
    board_strings = data.split("\n\n")
    boards = [Board(board_str) for board_str in board_strings]
    ans1 = sum(board.get_reflection_score() for board in boards)
    print(ans1)


if __name__ == "__main__":
    main()
