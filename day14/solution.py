from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
import itertools
from pprint import pprint
from typing import Iterable


TEST_INPUT = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""

TEST_INPUT_NORTH = """\
OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#....
"""


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def opposite(self):
        match self:
            case Direction.NORTH:
                return Direction.SOUTH
            case Direction.EAST:
                return Direction.WEST
            case Direction.SOUTH:
                return Direction.NORTH
            case Direction.WEST:
                return Direction.EAST


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def shift(self, direction, tiles=1):
        if direction == Direction.NORTH:
            return Point(self.x, self.y - tiles)
        elif direction == Direction.EAST:
            return Point(self.x + tiles, self.y)
        elif direction == Direction.SOUTH:
            return Point(self.x, self.y + tiles)
        elif direction == Direction.WEST:
            return Point(self.x - tiles, self.y)
        else:
            raise ValueError(f"Invalid direction {direction}")


class Tile(Enum):
    EMPTY = 0
    BLOCKER = 1
    ROLLER = 2

    def from_char(c):
        if c == "O":
            return Tile.ROLLER
        elif c == "#":
            return Tile.BLOCKER
        else:
            return Tile.EMPTY

    def __str__(self):
        if self == Tile.ROLLER:
            return "O"
        elif self == Tile.BLOCKER:
            return "#"
        else:
            return "."

    def __repr__(self) -> str:
        return str(self)


class Board:
    def __init__(self, input_str: str) -> None:
        self.roller_locs = set()
        self.blocker_locs = set()
        for y, line in enumerate(input_str.splitlines()):
            for x, c in enumerate(line):
                match Tile.from_char(c):
                    case Tile.ROLLER:
                        self.roller_locs.add(Point(x, y))
                    case Tile.BLOCKER:
                        self.blocker_locs.add(Point(x, y))
        self.height = y + 1
        self.width = x + 1

    def in_bounds(self, loc: Point) -> bool:
        return 0 <= loc.x < self.width and 0 <= loc.y < self.height

    def look(self, loc: Point, direction: Direction) -> (Point, int):
        num_rollers = 0
        while True:
            loc = loc.shift(direction)
            if not self.in_bounds(loc) or loc in self.blocker_locs:
                return loc, num_rollers
            elif loc in self.roller_locs:
                num_rollers += 1

    def border(self, direction: Direction) -> Iterable[Point]:
        match direction:
            case Direction.NORTH:
                return (Point(x, -1) for x in range(self.width))
            case Direction.EAST:
                return (Point(self.width, y) for y in range(self.height))
            case Direction.SOUTH:
                return (Point(x, self.height) for x in range(self.width))
            case Direction.WEST:
                return (Point(-1, y) for y in range(self.height))

    def tilt(self, direction: Direction) -> None:
        new_roller_locs = set()
        for loc in itertools.chain(self.border(direction), self.blocker_locs):
            stop, num_rollers = self.look(loc, direction.opposite())
            for i in range(num_rollers):
                new_roller_locs.add(loc.shift(direction.opposite(), i + 1))
        self.roller_locs = new_roller_locs

    def calculate_load(self) -> int:
        return sum(self.height - loc.y for loc in self.roller_locs)

    def find_cycle_loop(self):
        step = 0
        seen = {frozenset(self.roller_locs): step}
        while True:
            self.cycle(1)
            step += 1
            if step % 10 == 0:
                print(".", end="", flush=True)
            s = seen.setdefault(frozenset(self.roller_locs), step)
            if s != step:
                return step, s, self.calculate_load()

    def cycle(self, count):
        for _ in range(count):
            self.tilt(Direction.NORTH)
            self.tilt(Direction.WEST)
            self.tilt(Direction.SOUTH)
            self.tilt(Direction.EAST)

    def at(self, loc: Point) -> Tile:
        if loc in self.roller_locs:
            return Tile.ROLLER
        elif loc in self.blocker_locs:
            return Tile.BLOCKER
        else:
            return Tile.EMPTY

    def __repr__(self) -> str:
        return "\n".join(
            "".join(str(self.at(Point(x, y))) for x in range(self.width))
            for y in range(self.height)
        )


def main():
    # data = TEST_INPUT
    data = open("input").read()
    board1 = Board(data)
    print(board1)
    print()
    board1.tilt(Direction.NORTH)
    print(board1)
    print(board1.calculate_load())

    board2 = Board(data)
    cycle_end, cycle_start, _ = board2.find_cycle_loop()
    print("found loop:", cycle_start, cycle_end)
    short_count = (1000000000 - cycle_start) % (cycle_end - cycle_start)
    board2.cycle(short_count)
    print(board2.calculate_load())


if __name__ == "__main__":
    main()
