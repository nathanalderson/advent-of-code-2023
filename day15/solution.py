from dataclasses import dataclass
from pprint import pprint
import re

TEST_DATA = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"


class Operation:
    def __init__(self, label: str, op: str, focal_length: str | None) -> None:
        self.label = label
        self.op = op
        if focal_length:
            self.focal_length = int(focal_length)
        else:
            self.focal_length = None

    def __repr__(self) -> str:
        return f"{self.label}{self.op}{self.focal_length or ''}"


def parse_cmd(cmd: str) -> (str, Operation):
    m = re.match(r"(\w+)([-=])(\d*)", cmd)
    label, op_str, focal_length = m.groups()
    if focal_length == "":
        focal_length = None
    return Operation(label, op_str, focal_length)


def hash(s: str) -> int:
    v = 0
    for c in s:
        v += ord(c)
        v *= 17
        v %= 256
    return v


@dataclass
class Lens:
    label: str
    focal_length: int

    def __repr__(self) -> str:
        return f"<{self.label} {self.focal_length}>"


class Box:
    def __init__(self, num: int):
        self.num = num
        self.slots: list[Lens] = []

    def set(self, label: str, focal_length: int):
        _, lens = self.find_lens(label)
        if lens is not None:
            lens.focal_length = focal_length
        else:
            self.slots.append(Lens(label, focal_length))

    def remove(self, label: str):
        idx, _ = self.find_lens(label)
        if idx is not None:
            self.slots.pop(idx)

    def find_lens(self, label: str) -> (int, Lens):
        if idx := next((lens for lens in self.slots if lens.label == label), None):
            return idx, self.slots[idx]
        else:
            return None, None

    def __str__(self) -> str:
        return f"Box {self.num}: {self.slots}"

    def __repr__(self) -> str:
        return str(self)


class Boxes:
    def __init__(self):
        self.boxes = [Box(i) for i in range(256)]

    def do_operation(self, op: Operation):
        box = self.boxes[hash(op.label)]
        if op.op == "=":
            box.set(op.label, op.focal_length)
        elif op.op == "-":
            box.remove(op.label)
        else:
            raise ValueError(f"Unknown operation {op.op}")

    def __repr__(self) -> str:
        return "\n".join(str(box) for box in self.boxes if box.slots)


def run_initialization(ops: list[Operation]) -> Boxes:
    boxes = Boxes()
    for op in ops:
        if op.op == "-":
            boxes.boxes[hash(op.label)].slots.append(Lens(op.label, op.focal_length))
    return boxes


def main():
    # data = open("input").read().strip()
    data = TEST_DATA
    ans1 = sum(hash(s) for s in data.split(","))
    print(ans1)
    ops = (parse_cmd(cmd) for cmd in data.split(","))
    boxes = run_initialization(ops)
    pprint(boxes)


if __name__ == "__main__":
    main()
