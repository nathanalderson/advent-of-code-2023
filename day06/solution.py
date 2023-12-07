from pprint import pprint
from functools import reduce

INPUT = """\
Time:        41     96     88     94
Distance:   214   1789   1127   1055
"""

TEST_INPUT = """\
Time:      7  15   30
Distance:  9  40  200
"""


def parse_input(input) -> list[(int, int)]:
    lines = input.splitlines()
    time = [int(x) for x in lines[0].split()[1:]]
    distance = [int(x) for x in lines[1].split()[1:]]
    return list(zip(time, distance))


def get_distance(race_time, button_time):
    return button_time * (race_time - button_time)


def num_ways_to_win(race_time, record):
    distances = (get_distance(race_time, i) for i in range(race_time))
    winning_distances = (d for d in distances if d > record)
    return sum(1 for d in winning_distances)


def part1(race_infos):
    num_ways = [num_ways_to_win(race_time, record) for race_time, record in race_infos]
    return reduce(lambda x, y: x * y, num_ways)


def binary_search_min(time, min_dist):
    left = 0
    right = time
    while left < right:
        mid = (left + right) // 2
        if get_distance(time, mid) > min_dist:
            right = mid
        else:
            left = mid + 1
    return left


def binary_search_max(time, min_dist):
    left = 0
    right = time
    while left < right:
        mid = (left + right + 1) // 2
        if get_distance(time, mid) > min_dist:
            left = mid
        else:
            right = mid - 1
    return left


def part2(time, min_dist):
    min_button_time = binary_search_min(time, min_dist)
    max_button_time = binary_search_max(time, min_dist)
    return max_button_time - min_button_time + 1


print(part1(parse_input(INPUT)))
print(part2(41968894, 214178911271055))
