from __future__ import annotations
from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import Any

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


@dataclass(order=True)
class PrioritizedItem:
    priority: float
    item: Any = field(compare=False)


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
        case _:
            raise ValueError(f"Unknown direction: {direction}")


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
            case _:
                raise ValueError(f"Unknown direction: {direction}")

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"


@dataclass(frozen=True)
class Pos:
    point: Point
    direction: str
    straight_count: int

    def go(self, direction: str) -> Pos:
        return Pos(
            self.point.go(direction),
            direction,
            max(0, self.calc_straight_count(direction)),
        )

    def allowed_directions(self) -> list[str]:
        allowed = [turn(self.direction, "L"), turn(self.direction, "R")]
        if self.straight_count < 3:
            allowed.append(self.direction)
        return allowed

    def neighbors(self) -> list[Pos]:
        return [self.go(d) for d in self.allowed_directions()]

    def calc_straight_count(self, going_dir: str) -> int:
        if self.straight_count == -1:
            return 1
        elif self.direction == going_dir:
            return self.straight_count + 1
        else:
            return 1

    def __repr__(self) -> str:
        return f"<{self.point}, {self.direction}, {self.straight_count}>"


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

    def in_bounds(self, pos: Pos) -> bool:
        return 0 <= pos.point.x < self.width and 0 <= pos.point.y < self.height

    def neighbors(self, pos: Pos) -> list[Pos]:
        return [l for l in pos.neighbors() if self.in_bounds(l)]

    def cost(self, from_pos: Pos, to_pos: Pos) -> float:
        return self.costs[to_pos.point]

    def draw(self, path: list[Point]) -> None:
        path_set = set(path)
        for y in range(self.height):
            for x in range(self.width):
                p = Point(x, y)
                if p in path_set:
                    print(self.costs[p], end="")
                else:
                    print(".", end="")
            print()

    def draw_costs(self, costs: CostDict) -> None:
        for y in range(self.height):
            for x in range(self.width):
                p = Point(x, y)
                cost, _ = costs.get(p, (None, None))
                if cost:
                    print(f"{cost:3}|", end="")
                else:
                    print(" . |", end="")
            print()


def heuristic(a: Pos, b: Point) -> float:
    # return abs(a.point.x - b.x) + abs(a.point.y - b.y)
    return 0


CostDict = dict[Point, tuple[float, int]]


def a_star(board: Board, start: Pos, goal: Point):
    frontier = PriorityQueue()
    frontier.put(PrioritizedItem(0, start))
    came_from: dict[Point, Point | None] = {}
    cost_so_far: CostDict = {}
    came_from[start.point] = None
    cost_so_far[start.point] = 0, 0

    while not frontier.empty():
        current: Pos = frontier.get().item

        # print(current, board.neighbors(current))
        if current.point == goal:
            break

        for next in board.neighbors(current):
            new_cost, new_straight_count = cost_so_far[current.point]
            new_cost += board.cost(current, next)
            next_cost, next_straight_count = cost_so_far.get(
                next.point, (float("inf"), float("inf"))
            )
            if (
                next.point not in cost_so_far
                or new_cost < next_cost
                or (new_cost == next_cost and new_straight_count < next_straight_count)
            ):
                cost_so_far[next.point] = new_cost, new_straight_count
                priority = new_cost + heuristic(next, goal)
                frontier.put(PrioritizedItem(priority, next))
                came_from[next.point] = current.point

    return came_from, cost_so_far


def reconstruct_path(
    came_from: dict[Point, Point | None],
    cost_so_far: CostDict,
    goal: Point,
) -> tuple[list[Point], float]:
    current = goal
    path = [current]
    while True:
        current = came_from[current]
        if current is not None:
            path.append(current)
        else:
            break
    path.reverse()
    return path, cost_so_far[goal][0]


def main():
    input = TEST_INPUT
    board = Board(input)
    goal = Point(board.width - 1, board.height - 1)
    came_from, cost_so_far = a_star(board, Pos(Point(0, 0), "E", -1), goal)
    path, cost = reconstruct_path(came_from, cost_so_far, goal)
    print("Path:", path, "Cost:", cost)
    board.draw(path)
    board.draw_costs(cost_so_far)


if __name__ == "__main__":
    main()
