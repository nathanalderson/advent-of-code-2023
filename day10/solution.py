import math
from pprint import pprint

TEST_INPUT1 = """\
.....
.S-7.
.|.|.
.L-J.
.....
"""


class Maze:
    def __init__(self, lines):
        self.maze = lines
        self.height = len(lines)
        self.width = len(lines[0])
        self.start_loc = self.find_start()

    def __getitem__(self, pos):
        row, col = pos
        return self.maze[row][col]

    def __str__(self):
        return "\n".join("".join(row) for row in self.maze)

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

    def draw_path(self, path):
        for r in range(self.height):
            for c in range(self.width):
                if (r, c) in path:
                    print(self[r, c], end="")
                else:
                    print(".", end="")
            print()


def main():
    # lines = TEST_INPUT1.splitlines()
    lines = open("input").readlines()
    maze = Maze(lines)
    path = list(maze.traverse())
    ans1 = math.ceil(len(path) / 2)
    print(ans1)
    # print(maze.draw_path(path))


if __name__ == "__main__":
    main()
