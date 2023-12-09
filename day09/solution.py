from pprint import pprint
from itertools import *
from functools import *

TEST_INPUT = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""


def parse_line(line):
    return [int(x) for x in line.split()]


def get_next_val(seq: [int]):
    if all(x == 0 for x in seq):
        return 0
    lower_next_val = get_next_val([x2 - x1 for x1, x2 in pairwise(seq)])
    return seq[-1] + lower_next_val


def get_prev_val(seq: [int]):
    if all(x == 0 for x in seq):
        return 0
    lower_prev_val = get_prev_val([x2 - x1 for x1, x2 in pairwise(seq)])
    return seq[0] - lower_prev_val


def main():
    # lines = TEST_INPUT.splitlines()
    with open("input") as f:
        lines = f.readlines()
    seqs = [parse_line(line) for line in lines]
    next_vals = [get_next_val(seq) for seq in seqs]
    ans1 = sum(next_vals)
    print(ans1)
    prev_vals = [get_prev_val(seq) for seq in seqs]
    ans2 = sum(prev_vals)
    print(ans2)


if __name__ == "__main__":
    main()
