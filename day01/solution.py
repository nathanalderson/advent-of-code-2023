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


def has_digit(line: str, allow_words=False):
    if line == "":
        return None
    elif line[0].isdigit():
        return line[0]
    elif line[-1].isdigit():
        return line[-1]
    elif allow_words:
        for word, digit in REPLACEMENTS.items():
            if line.find(word) != -1:
                return digit
    return None


def forward_fragments(line):
    for i in range(len(line)):
        yield line[: i + 1]


def reverse_fragments(line):
    r = line[::-1]
    for i in range(len(line)):
        yield r[: i + 1][::-1]


def search(fragments, allow_words):
    for fragment in fragments:
        if d := has_digit(fragment, allow_words):
            return d
    raise ValueError("No digits in line")


def process(line: str, allow_words):
    first_digit = search(forward_fragments(line), allow_words)
    last_digit = search(reverse_fragments(line), allow_words)
    return int(f"{first_digit}{last_digit}")


def solve(input, allow_words):
    return sum([process(line, allow_words) for line in input.splitlines()])


def main():
    with open("input.txt", "r") as f:
        input = f.read()
    print(solve(input, allow_words=False))
    print(solve(input, allow_words=True))


if __name__ == "__main__":
    main()
