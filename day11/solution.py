import itertools
from pprint import pprint


TEST_INPUT = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""


def expand(locs, expansion_factor):
    present_rows = set(r for r, _ in locs)
    present_cols = set(c for _, c in locs)
    for r, c in locs:
        num_empty_rows_before = r - sum(1 for pr in present_rows if pr < r)
        num_empty_cols_before = c - sum(1 for pc in present_cols if pc < c)
        yield (
            r + (num_empty_rows_before * (expansion_factor - 1)),
            c + (num_empty_cols_before * (expansion_factor - 1)),
        )


def dist(loc1, loc2):
    return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])


def sumdist(locs):
    return sum(dist(loc1, loc2) for loc1, loc2 in itertools.combinations(locs, 2))


def main():
    # board = [line.strip() for line in TEST_INPUT.splitlines()]
    board = open("input").readlines()
    locs = [
        (r, c)
        for r, row in enumerate(board)
        for c, cell in enumerate(row)
        if cell == "#"
    ]
    expanded_part1 = list(expand(locs, expansion_factor=2))
    print(sumdist(expanded_part1))
    expanded_part2 = list(expand(locs, expansion_factor=1_000_000))
    print(sumdist(expanded_part2))


if __name__ == "__main__":
    main()
