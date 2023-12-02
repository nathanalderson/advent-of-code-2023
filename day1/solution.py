import functools


def process1(line):
    first_digit = next(c for c in line if c.isdigit())
    last_digit = next(c for c in reversed(line) if c.isdigit())
    return int(f"{first_digit}{last_digit}")


REPLACEMENTS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def start_digit(line):
    if line == "":
        raise ValueError("No digits in line")
    elif line[0].isdigit():
        return line[0]
    else:
        for word, digit in REPLACEMENTS.items():
            if line.startswith(word):
                return digit
        return None


def forward(line):
    while line != "":
        if d := start_digit(line):
            return d
        else:
            line = line[1:]


def reverse_fragments(line):
    r = line[::-1]
    for i in range(len(line)):
        yield r[: i + 1][::-1]


def backward(line):
    for fragment in reverse_fragments(line):
        if d := start_digit(fragment):
            return d
    raise ValueError("No digits in line")


def process2(line: str):
    first_digit = forward(line)
    last_digit = backward(line)
    return int(f"{first_digit}{last_digit}")


def part1(input):
    return sum([process1(line) for line in input.splitlines()])


def part2(input):
    return sum([process2(line) for line in input.splitlines()])


def main():
    with open("input.txt", "r") as f:
        input = f.read()
    print(part1(input))
    print(part2(input))


if __name__ == "__main__":
    main()
