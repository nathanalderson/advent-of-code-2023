from pprint import pprint
from dataclasses import dataclass
import re

TEST_INPUT = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""


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

    def __repr__(self):
        return f"({self.x}, {self.y})"


@dataclass(frozen=True)
class Thing:
    points: list[Point]

    @property
    def first_point(self):
        return self.points[0]

    def adjacent_points(self):
        return set(flatten(p.adjacent_points() for p in self.points)) - set(self.points)


@dataclass(frozen=True)
class Symbol(Thing):
    char: str

    def __repr__(self):
        return f"{self.char}@{self.first_point}"


@dataclass(frozen=True)
class Number(Thing):
    value: int

    def __repr__(self):
        return f"{self.value}@{self.first_point}"


@dataclass
class Node:
    thing: Thing
    edges: list["Edge"]

    def __repr__(self):
        return f"Node< {self.thing} >"

    def connects_to(self):
        return [e.other_node(self) for e in self.edges]

    def is_partnumber(self):
        return isinstance(self.thing, Number) and any(
            isinstance(n.thing, Symbol) for n in self.connects_to()
        )

    def gear_ratio(self):
        if isinstance(self.thing, Symbol) and self.thing.char == "*":
            if len(self.edges) == 2:
                return mult(e.other_node(self).thing.value for e in self.edges)
        return 0


def mult(iterable):
    result = 1
    for i in iterable:
        result *= i
    return result


@dataclass
class Edge:
    node1: Node
    node2: Node

    def __repr__(self):
        return f"Edge<{self.node1} <-> {self.node2}>"

    def other_node(self, node):
        if node == self.node1:
            return self.node2
        elif node == self.node2:
            return self.node1
        else:
            raise ValueError(f"Node {node} not in edge {self}")


@dataclass
class Graph:
    nodes: dict[Point, Node]

    def get_or_add(self, thing: Thing):
        if node := self.nodes.get(thing.first_point):
            return node
        node = Node(thing, [])
        self.nodes[thing.first_point] = node
        return node

    def connect(self, thing1: Thing, thing2: Thing):
        node1 = self.get_or_add(thing1)
        node2 = self.get_or_add(thing2)
        edge = Edge(node1, node2)
        node1.edges.append(edge)
        node2.edges.append(edge)


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


def part1(graph: Graph):
    part_numbers = [n for n in graph.nodes.values() if n.is_partnumber()]
    return sum(n.thing.value for n in part_numbers)


def part2(graph):
    return sum(n.gear_ratio() for n in graph.nodes.values())


def build_graph(numbers, symbols):
    graph = Graph({})
    symbols_by_location = {p: s for s in symbols for p in s.points}
    for n in numbers:
        for p in n.adjacent_points():
            if s := symbols_by_location.get(p):
                graph.connect(n, s)
    return graph


def main():
    with open("input") as f:
        lines = f.readlines()
    # lines = TEST_INPUT.splitlines()
    symbols = list(parse_symbols(lines))
    numbers = list(parse_numbers(lines))
    graph = build_graph(numbers, symbols)
    pprint(graph)
    print(part1(graph))
    print(part2(graph))
    # answers: 550934, 81997870


if __name__ == "__main__":
    main()
