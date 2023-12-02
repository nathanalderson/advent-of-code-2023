import re
from dataclasses import dataclass


@dataclass
class Collection:
    reds: int
    greens: int
    blues: int


@dataclass
class Game:
    game_number: int
    collections: list[Collection]

    def is_possible(self, reds, greens, blues):
        reds_possible = all(collection.reds <= reds for collection in self.collections)
        greens_possible = all(
            collection.greens <= greens for collection in self.collections
        )
        blues_possible = all(
            collection.blues <= blues for collection in self.collections
        )
        return reds_possible and greens_possible and blues_possible

    def power(self):
        required_reds = max(collection.reds for collection in self.collections)
        required_greens = max(collection.greens for collection in self.collections)
        required_blues = max(collection.blues for collection in self.collections)
        return required_reds * required_greens * required_blues


def parse_color(collection, color):
    if m := re.search(rf"(\d+) {color}", collection):
        return int(m.group(1))
    else:
        return 0


def parse_collection(collection):
    reds = parse_color(collection, "red")
    greens = parse_color(collection, "green")
    blues = parse_color(collection, "blue")
    return Collection(reds, greens, blues)


def parse(line):
    game_part, collections_part = line.split(": ")
    game_num = int(game_part.split(" ")[1])
    collections = [
        parse_collection(collection) for collection in collections_part.split("; ")
    ]
    return Game(game_num, collections)


def part1(games):
    possible_games = (game for game in games if game.is_possible(12, 13, 14))
    return sum(game.game_number for game in possible_games)


def part2(games):
    return sum(game.power() for game in games)


def main():
    with open("input") as f:
        lines = f.readlines()
    games = [parse(line) for line in lines]
    print(part1(games))
    print(part2(games))


if __name__ == "__main__":
    main()
