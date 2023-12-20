import dataclasses
import re
from dataclasses import dataclass
from pprint import pprint

TEST_INPUT = """\
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""


@dataclass(frozen=True)
class Part:
    x: int
    m: int
    a: int
    s: int

    def score(self):
        return self.x + self.m + self.a + self.s


@dataclass(frozen=True)
class PartRange:
    x: range
    m: range
    a: range
    s: range

    def score(self):
        return len(self.x) * len(self.m) * len(self.a) * len(self.s)


def parse_part(line: str):
    if m := re.match(r"{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}", line):
        return Part(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)))
    else:
        raise ValueError(line)


class Workflow:
    def __init__(self, line: str) -> None:
        if m := re.match(r"(\w+){(.*)}", line):
            self.name = m.group(1)
            self.steps = m.group(2).split(",")

    def __repr__(self) -> str:
        return f"{self.name}{self.steps}"


OPERATORS = {
    ">": lambda a, b: a > b,
    "<": lambda a, b: a < b,
}

RANGE_OPERATORS = {
    "<": lambda r, val: (range(r.start, val), range(val, r.stop)),
    ">": lambda r, val: (range(val + 1, r.stop), range(r.start, val + 1)),
}


def accepted(part: Part, workflows: dict[str, Workflow]) -> bool:
    goto = "in"
    while True:
        if goto == "A":
            return True
        if goto == "R":
            return False
        workflow = workflows[goto]
        for step in workflow.steps:
            if m := re.match(r"([xmas])([><])(\d+):(\w+)", step):
                category, operator, val, dest = m.groups()
                op = OPERATORS[operator]
                if op(getattr(part, category), int(val)):
                    goto = dest
                    break
            else:
                goto = step


def route_ranges(workflows: dict[str, Workflow]) -> int:
    to_route: list[tuple[PartRange, str]] = [
        (
            PartRange(range(1, 4001), range(1, 4001), range(1, 4001), range(1, 4001)),
            "in",
        )
    ]
    count = 0
    while to_route:
        part_range, goto = to_route.pop()
        if goto == "A":
            count += part_range.score()
            continue
        if goto == "R":
            continue
        workflow = workflows[goto]
        for step in workflow.steps:
            if m := re.match(r"([xmas])([><])(\d+):(\w+)", step):
                category, operator, val, dest = m.groups()
                op = RANGE_OPERATORS[operator]
                matching_range, nonmatching_range = op(
                    getattr(part_range, category), int(val)
                )
                if matching_range:
                    p = dataclasses.replace(part_range, **{category: matching_range})
                    to_route.append((p, dest))
                if nonmatching_range:
                    part_range = dataclasses.replace(
                        part_range, **{category: nonmatching_range}
                    )
            else:
                to_route.append((part_range, step))
    return count


def main():
    # data = TEST_INPUT
    data = open("input").read()
    workflow_part, parts_part = data.split("\n\n")
    parts = [parse_part(line) for line in parts_part.splitlines()]
    workflows = (Workflow(line) for line in workflow_part.splitlines())
    workflows = {w.name: w for w in workflows}
    accepted_parts = [part for part in parts if accepted(part, workflows)]
    ans1 = sum(part.score() for part in accepted_parts)
    print(ans1)

    ans2 = route_ranges(workflows)
    print(ans2)


if __name__ == "__main__":
    main()
