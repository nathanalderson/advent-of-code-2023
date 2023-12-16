from dataclasses import dataclass
from typing import Any


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


class Tile:
    def __init__(self, c: str) -> None:
        self.c = c

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

    def __str__(self) -> str:
        return "\n".join(
            "".join(str(self.tiles.get(Point(x, y), ".")) for x in range(self.width))
            for y in range(self.height)
        )


def main():
    board = Board(TEST_INPUT.strip())
    print(board)


if __name__ == "__main__":
    main()
