from __future__ import annotations
from dataclasses import dataclass
import itertools
import math
from pprint import pprint
import re

TEST_INPUT = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""


@dataclass(frozen=True)
class Map:
    name: str
    mappings: tuple((range, range))  # tuple(dest_range, source_range)

    def parse(name, lines) -> Map:
        ranges = tuple(Map.parse_range(line) for line in lines)
        return Map(name, ranges)

    def parse_range(line) -> (range, range):
        source_start, dest_start, length = [int(x) for x in line.split()]
        return range(source_start, source_start + length), range(
            dest_start, dest_start + length
        )

    def __getitem__(self, key: int):
        for dest_range, source_range in self.mappings:
            if key in source_range:
                return dest_range[key - source_range.start]
        return key


@dataclass(frozen=True)
class Data:
    seeds: tuple(int)
    maps: tuple(Map)

    def parse(input) -> Data:
        seeds_line = re.search(r"seeds: (.*)", input)
        seeds = tuple(int(x) for x in seeds_line.group(1).split())
        map_blocks = re.findall(r"([a-z-]+?) map:\n(.*?)(?:\n\n|$)", input, re.DOTALL)
        maps = tuple(Map.parse(name, lines.splitlines()) for name, lines in map_blocks)
        return Data(seeds, maps)

    def seed_location(self, seed: int) -> int:
        location = seed
        for map in self.maps:
            location = map[location]
        return location

    def nearest_seed_location(self) -> int:
        return min(self.seed_location(seed) for seed in self.seeds)

    def nearest_seed_location_range_version(self) -> int:
        seed_ranges = [
            range(start, start + count)
            for start, count in itertools.batched(self.seeds, 2)
        ]
        print("total seeds:", sum(len(seed_range) for seed_range in seed_ranges))
        # return min(self.seed_location(seed) for seed in itertools.chain(*seed_ranges))
        closest = math.inf
        for i, seed in enumerate(itertools.chain(*seed_ranges)):
            if i % 100000 == 0:
                print(i)
            location = self.seed_location(seed)
            if location < closest:
                closest = location
        return closest


def main():
    # input = TEST_INPUT
    with open("input") as f:
        input = f.read()
    data = Data.parse(input)
    print(data.nearest_seed_location())
    print(data.nearest_seed_location_range_version())


if __name__ == "__main__":
    main()
