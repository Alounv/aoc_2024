import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utilities.parse import get_lines

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logic ---


class Block:
    def __init__(self, id: int, size: int):
        self.id = id
        self.size = size

    def pop(self) -> tuple[int, bool]:
        self.size -= 1
        empty = self.size == 0
        return self.id, empty

    def grow(self) -> None:
        self.size += 1

    def __str__(self):
        return f"{self.id}: {self.size}"


class BlockList:
    def __init__(self, input: str):
        self.blocks: list[Block] = []
        for i in range(len(input)):
            size = int(input[i])
            if size == 0:
                continue
            id = i // 2 if (i % 2 == 0) else -1
            self.blocks.append(Block(id, size))

    def __str__(self):
        result = ""
        for b in self.blocks:
            c = "." if b.id == -1 else str(b.id)
            result += c * b.size
        return result

    def size(self):
        return len(self.blocks)

    def insert(self, i: int, id: int, size: int = 1):
        self.blocks.insert(i, Block(id, size))

    def remove(self, i: int):
        self.blocks.pop(i)

    def pop(self):
        return self.blocks.pop()

    def last(self):
        return self.blocks[-1]

    def get(self, i: int):
        return self.blocks[i]


def parse(input: str) -> BlockList:
    return BlockList(input)


def arrange(list: BlockList, start_i: int) -> None:
    i = start_i

    while i < list.size():
        # remove last block if empty
        if list.last().id == -1:
            list.pop()
            continue

        # if not empty, move to next block
        if list.get(i).id != -1:
            i += 1
            continue

        # take last block id
        id, empty = list.last().pop()
        if empty:
            list.pop()

        # if same id, merge in empty prev block else create block
        prev = list.get(i - 1)
        if prev.id == id:
            list.get(i - 1).grow()
        else:
            list.insert(i, id)
            i += 1

        # remove slot in empty block
        _, empty = list.get(i).pop()
        if empty:
            list.remove(i)
            i += 1


def calc(list: BlockList) -> int:
    sum = 0
    p = 0
    for b in list.blocks:
        for i in range(b.size):
            sum += p * b.id
            p += 1
    return sum


def logic(input: str) -> int:
    lines = get_lines(input)
    list = parse(lines[0])
    arrange(list, 0)
    return calc(list)


# --- Example ---


def test_example_1():
    example = "12345"
    list = parse(example)
    assert str(list) == "0..111....22222"


def test_example_2():
    example = "2333133121414131402"
    list = parse(example)
    assert str(list) == "00...111...2...333.44.5555.6666.777.888899"
    arrange(list, 1)
    assert str(list) == "0099811188827773336446555566"


def test_example_3():
    example = "233313312141413140213"
    list = parse(example)
    assert str(list) == "00...111...2...333.44.5555.6666.777.888899.101010"
    arrange(list, 1)
    assert str(list) == "0010101011199828883337447555576666"


def test_example_4():
    example = "233313312141413140213"
    assert logic(example) == 2584


def test_example_5():
    example = "000000000000000000101"
    assert logic(example) == 10


# --- Input ---


def test_input():
    result = logic(input)
    assert result == 6366665108136
