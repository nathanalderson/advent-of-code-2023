TEST_DATA = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"


def checksum(cmd: str) -> int:
    v = 0
    for c in cmd:
        v += ord(c)
        v *= 17
        v %= 256
    return v


def main():
    data = open("input").read().strip()
    # data = TEST_DATA
    ans1 = sum(checksum(cmd) for cmd in data.split(","))
    print(ans1)


if __name__ == "__main__":
    main()
