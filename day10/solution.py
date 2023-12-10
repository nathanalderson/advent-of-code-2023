import math
from pprint import pprint

TEST_INPUT1 = """\
.....
.S-7.
.|.|.
.L-J.
.....
"""


def is_outside_test(row, col, quadrant):
    if row == 0 or row == 4:
        return True
    if col == 0 or col == 4:
        return True
    if row == 1 and "N" in quadrant:
        return True
    if row == 3 and "S" in quadrant:
        return True
    if col == 1 and "W" in quadrant:
        return True
    if col == 3 and "E" in quadrant:
        return True
    return False


class Maze:
    def __init__(self, lines):
        self.maze = lines
        self.height = len(lines)
        self.width = len(lines[0])
        self.start_loc = self.find_start()
        self.path = list(self.traverse())
        self.path_set = set(self.path)

    def __getitem__(self, loc):
        row, col = loc
        return self.maze[row][col]

    def __setitem__(self, loc, val):
        row, col = loc
        s = self.maze[row]
        self.maze[row] = s[:col] + val + s[col + 1 :]

    def __str__(self):
        return "\n".join("".join(row) for row in self.maze)

    def in_bounds(self, row, col):
        return 0 <= row < self.height and 0 <= col < self.width

    def find_start(self):
        for row in range(self.height):
            for col in range(self.width):
                if self[row, col] == "S":
                    return row, col

    def traverse(self):
        loc = self.start_loc
        [d1, d2] = list(self.find_start_connections())
        dir = d1
        end = Maze.move(loc, d2)
        while loc != end:
            loc, dir = self.follow(loc, dir)
            yield loc

    def find_start_connections(self):
        if self[Maze.move(self.start_loc, "N")] in ("|", "F", "7"):
            yield "N"
        if self[Maze.move(self.start_loc, "S")] in ("|", "J", "L"):
            yield "S"
        if self[Maze.move(self.start_loc, "E")] in ("-", "7", "J"):
            yield "E"
        if self[Maze.move(self.start_loc, "W")] in ("-", "F", "L"):
            yield "W"

    def replace_start(self):
        row, col = self.start_loc
        [d1, d2] = sorted(self.find_start_connections())
        match d1, d2:
            case "N", "S":
                self[row, col] = "|"
            case "E", "W":
                self[row, col] = "-"
            case "E", "N":
                self[row, col] = "L"
            case "N", "W":
                self[row, col] = "J"
            case "E", "S":
                self[row, col] = "F"
            case "S", "W":
                self[row, col] = "7"
            case _:
                raise ValueError("Invalid start: {} {}".format(d1, d2))

    def follow(self, loc, dir):
        match dir, self[loc]:
            case "N", "|":
                new_dir = "N"
            case "N", "F":
                new_dir = "E"
            case "N", "7":
                new_dir = "W"
            case "S", "|":
                new_dir = "S"
            case "S", "J":
                new_dir = "W"
            case "S", "L":
                new_dir = "E"
            case "E", "-":
                new_dir = "E"
            case "E", "7":
                new_dir = "S"
            case "E", "J":
                new_dir = "N"
            case "W", "-":
                new_dir = "W"
            case "W", "F":
                new_dir = "S"
            case "W", "L":
                new_dir = "N"
            case d, "S":
                new_dir = d
            case d, l:
                raise ValueError("Invalid follow: {} {}".format(d, l))
        return Maze.move(loc, new_dir), new_dir

    def move(loc, direction):
        row, col = loc
        match direction:
            case "N":
                return row - 1, col
            case "S":
                return row + 1, col
            case "E":
                return row, col + 1
            case "W":
                return row, col - 1
            case _:
                raise ValueError("Invalid direction")

    def move_quadrant(row, col, quadrant, direction) -> tuple[int, int, str]:
        match quadrant, direction:
            case "NW", "N":
                return row - 1, col, "SW"
            case "NW", "W":
                return row, col - 1, "NE"
            case "NW", "S":
                return row, col, "SW"
            case "NW", "E":
                return row, col, "NE"
            case "NE", "N":
                return row - 1, col, "SE"
            case "NE", "E":
                return row, col + 1, "NW"
            case "NE", "S":
                return row, col, "SE"
            case "NE", "W":
                return row, col, "NW"
            case "SE", "S":
                return row + 1, col, "NE"
            case "SE", "E":
                return row, col + 1, "SW"
            case "SE", "N":
                return row, col, "NE"
            case "SE", "W":
                return row, col, "SW"
            case "SW", "S":
                return row + 1, col, "NW"
            case "SW", "W":
                return row, col - 1, "SE"
            case "SW", "N":
                return row, col, "NW"
            case "SW", "E":
                return row, col, "SE"
            case x:
                raise ValueError(f"Invalid direction: {x}")

    def draw_path(self, path):
        for r in range(self.height):
            for c in range(self.width):
                if (r, c) in path:
                    print("X", end="")
                else:
                    print(".", end="")
            print()

    # I'm going to subdivide each cell into quadrants NE, NW, SE, SW
    def reachable_neighbor_quadrants(
        self, from_quadrant: tuple[int, int, str]
    ) -> list[tuple[int, int, str]]:
        row, col, q = from_quadrant
        if (row, col) in self.path_set or (row, col) == self.start_loc:
            here = self[row, col]
        else:
            here = "."
        match here, q:
            case "|", ("NW" | "SW"):
                unreachable_dirs = "E"
            case "|", ("NE" | "SE"):
                unreachable_dirs = "W"
            case "-", ("NW" | "NE"):
                unreachable_dirs = "S"
            case "-", ("SW" | "SE"):
                unreachable_dirs = "N"
            case "7", "NW":
                unreachable_dirs = "S"
            case "7", "SE":
                unreachable_dirs = "W"
            case "7", "SW":
                unreachable_dirs = "NE"
            case "J", "NW":
                unreachable_dirs = "SE"
            case "J", "NE":
                unreachable_dirs = "W"
            case "J", "SW":
                unreachable_dirs = "N"
            case "F", "NE":
                unreachable_dirs = "S"
            case "F", "SE":
                unreachable_dirs = "NW"
            case "F", "SW":
                unreachable_dirs = "E"
            case "L", "NE":
                unreachable_dirs = "SW"
            case "L", "SE":
                unreachable_dirs = "N"
            case "L", "NW":
                unreachable_dirs = "E"
            case _:
                unreachable_dirs = ""
        reachable_dirs = set("NSEW") - set(unreachable_dirs)
        reachable_quadrants = (
            Maze.move_quadrant(row, col, q, dir) for dir in reachable_dirs
        )
        return (q for q in reachable_quadrants if self.in_bounds(q[0], q[1]))

    def reachable_cells(
        self, from_quadrant: tuple[int, int, str]
    ) -> list[tuple[int, int]]:
        self.replace_start()
        explored = set()
        to_explore = set([from_quadrant])
        while to_explore:
            q = to_explore.pop()
            explored.add(q)
            neighbors = set(self.reachable_neighbor_quadrants(q))
            new_neighbors = neighbors - explored
            to_explore.update(new_neighbors)
        return set((r, c) for r, c, q in explored)


def main():
    # lines = TEST_INPUT1.splitlines()
    lines = open("input").readlines()
    maze = Maze(lines)
    ans1 = math.ceil(len(maze.path) / 2)
    print(ans1)
    outside_cells = maze.reachable_cells((0, 0, "NW"))
    num_outside_cells = len(outside_cells)
    total_cells = maze.height * maze.width
    num_inside_cells = total_cells - num_outside_cells
    print(num_inside_cells)


if __name__ == "__main__":
    main()
