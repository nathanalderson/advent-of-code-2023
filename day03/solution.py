from pprint import pprint
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def adjacent_points(self):
        yield Point(self.x + 1, self.y)
        yield Point(self.x - 1, self.y)
        yield Point(self.x, self.y + 1)
        yield Point(self.x, self.y - 1)
        yield Point(self.x + 1, self.y + 1)
        yield Point(self.x + 1, self.y - 1)
        yield Point(self.x - 1, self.y + 1)
        yield Point(self.x - 1, self.y - 1)


@dataclass(frozen=True)
class Thing:
    points: list[Point]

    def adjacent_points(self):
        return set(flatten(p.adjacent_points() for p in self.points)) - set(self.points)


@dataclass(frozen=True)
class Symbol(Thing):
    char: str


@dataclass(frozen=True)
class Number(Thing):
    value: int


def parse_symbols(lines):
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c not in "0123456789.\n":
                yield Symbol([Point(x, y)], c)


def parse_numbers(lines):
    for y, line in enumerate(lines):
        for m in re.finditer(r"\d+", line):
            yield Number(
                [Point(x, y) for x in range(m.start(), m.end())],
                int(m[0]),
            )


def flatten(ll):
    return [i for l in ll for i in l]


def is_partnumber(number: Number, symbol_locs: set[Point]):
    return any(p in symbol_locs for p in number.adjacent_points())


def gear_ratio(symbol: Symbol, numbers: list[Number]):
    if symbol.char == "*":
        adjacent_numbers = [
            n for n in numbers if any(p in symbol.adjacent_points() for p in n.points)
        ]
        if len(adjacent_numbers) == 2:
            return adjacent_numbers[0].value * adjacent_numbers[1].value
    return 0


def part1(numbers: list[Number], symbols: list[Symbol]):
    symbol_locs = set(flatten(s.points for s in symbols))
    part_numbers = [n for n in numbers if is_partnumber(n, symbol_locs)]
    return part_numbers, sum(n.value for n in part_numbers)


def part2(numbers: list[Number], symbols: list[Symbol]):
    return sum(gear_ratio(s, numbers) for s in symbols)


def main():
    with open("input") as f:
        lines = f.readlines()
    symbols = list(parse_symbols(lines))
    numbers = list(parse_numbers(lines))
    part_numbers, ans1 = part1(numbers, symbols)
    print(ans1)
    print(part2(part_numbers, symbols))


if __name__ == "__main__":
    main()
