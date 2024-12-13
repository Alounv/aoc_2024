import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from day_09.test_09_1 import BlockList, parse
from utilities.parse import get_lines

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logic ---


def get_next_empty(list: BlockList, size: int, index: int) -> int:
    for i, b in enumerate(list.blocks):
        if i >= index:
            return -1
        if b.id == -1 and b.size >= size:
            return i
    return -1


def arrange(list: BlockList, start_i: int) -> None:
    bi = list.size() - 1

    while bi >= 0:
        if bi >= list.size():
            bi -= 1

        # remove last block if empty
        if list.last().id == -1:
            list.pop()
            continue

        block = list.get(bi)
        # if empty move to next block
        if block.id == -1:
            bi -= 1
            continue

        free_index = get_next_empty(list, block.size, bi)

        # if there is no available slot, move to next block
        if free_index == -1:
            bi -= 1
            continue

        # else move the block
        free = list.get(free_index)
        new_size = free.size - block.size

        if new_size == 0:
            # replace
            free.id = block.id
            block.id = -1
        else:
            # or insert
            list.insert(free_index, block.id, block.size)  # for block
            free.size = new_size
            bi += 1  # since we just added one block

        # remove block from list
        block.id = -1
        bi -= 1


def calc(list: BlockList) -> int:
    sum = 0
    p = 0

    for b in list.blocks:
        if b.id == -1:
            p += b.size
            continue

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
    example = "2333133121414131402"
    list = parse(example)
    assert str(list) == "00...111...2...333.44.5555.6666.777.888899"
    arrange(list, 1)
    assert str(list) == "00992111777.44.333....5555.6666.....8888"
    result = calc(list)
    assert result == 2858


def test_example_3():
    example = "233313312141413140213"
    list = parse(example)
    assert str(list) == "00...111...2...333.44.5555.6666.777.888899.101010"
    arrange(list, 1)
    assert str(list) == "00101010111992.777333.44.5555.6666.....8888"


# --- Input ---


def test_input():
    result = logic(input)
    assert result == 6398065450842
