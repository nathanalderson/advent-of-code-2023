from __future__ import annotations
from dataclasses import dataclass
from pprint import pprint
from typing import Iterable

TEST_INPUT = """\
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def neighbors(self) -> Iterable[Point]:
        yield Point(self.x + 1, self.y)
        yield Point(self.x - 1, self.y)
        yield Point(self.x, self.y + 1)
        yield Point(self.x, self.y - 1)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"


def parse(data: str) -> tuple[frozenset[Point], Point]:
    locs = {}
    start = None
    for y, line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            if char != "#":
                locs[Point(x, y)] = char
            if char == "S":
                start = Point(x, y)
    assert locs, "No locations found"
    assert start, "No start found"
    return frozenset(locs), start


def dfs(garden: Garden, start: Point, max_steps: int):
    stack: list[tuple[Point, int]] = [(start, 0)]
    seen: set[tuple[Point, int]] = set()
    while stack:
        pos, steps = stack.pop()
        if (pos, steps) in seen:
            continue
        seen.add((pos, steps))
        if steps == max_steps:
            yield pos
            continue
        stack.extend(
            (neighbor, steps + 1) for neighbor in pos.neighbors() if neighbor in garden
        )


class Garden:
    def __init__(self, locs: frozenset[Point], infinite: bool = False):
        self.locs = locs
        self.width = max(loc.x for loc in locs) + 1
        self.height = max(loc.y for loc in locs) + 1
        self.infinite = infinite

    def __contains__(self, point: Point) -> bool:
        if self.infinite:
            p = Point(point.x % self.width, point.y % self.height)
        else:
            p = point
        return p in self.locs


def main():
    # data = TEST_INPUT
    data = open("input").read()
    locs, start = parse(data)
    garden = Garden(locs)
    endpoints = dfs(garden, start, 64)
    ans1 = sum(1 for _ in endpoints)
    print(ans1)

    garden2 = Garden(locs, infinite=True)
    endpoints2 = dfs(garden2, start, 26501365)
    ans2 = sum(1 for _ in endpoints2)
    print(ans2)


if __name__ == "__main__":
    main()
