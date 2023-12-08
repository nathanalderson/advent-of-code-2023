from pprint import pprint
from itertools import *
from dataclasses import dataclass
import re

TEST_INPUT1 = """\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

TEST_INPUT2 = """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""

TEST_INPUT3 = """\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""


class Node:
    def __init__(self, line) -> None:
        m = re.match(r"(\w+) = \((\w+), (\w+)\)", line)
        self.name, self.left, self.right = m.groups()

    def __repr__(self) -> str:
        return f"<{self.name}>({self.left}, {self.right})"


class Puzzle:
    def __init__(self, lines) -> None:
        self.directions = lines[0].strip()
        nodes = (Node(line) for line in lines[2:])
        self.nodes = {node.name: node for node in nodes}

    def go(self, node, direction):
        if direction == "L":
            return self.nodes[node.left]
        elif direction == "R":
            return self.nodes[node.right]
        else:
            raise ValueError(f"Unknown direction: {direction}")

    def traverse(self):
        loc = self.nodes["AAA"]
        directions = cycle(self.directions)
        path = []
        while loc.name != "ZZZ":
            direction = next(directions)
            loc = self.go(loc, direction)
            path.append(loc)
        return path

    def multitraverse(self):
        locs = [node for name, node in self.nodes.items() if name.endswith("A")]
        directions = cycle(self.directions)
        steps = 0
        while not all(loc.name.endswith("Z") for loc in locs):
            direction = next(directions)
            steps += 1
            locs = [self.go(n, direction) for n in locs]
        return steps


def main():
    # lines = TEST_INPUT1.splitlines()
    # lines = TEST_INPUT2.splitlines()
    # lines = TEST_INPUT3.splitlines()
    with open("input") as f:
        lines = f.readlines()
    puzzle = Puzzle(lines)
    path = puzzle.traverse()
    print(path)
    print(len(path))
    print(puzzle.multitraverse())


if __name__ == "__main__":
    main()
