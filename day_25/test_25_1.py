import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities.parse import get_lines, get_parts

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()


def get_columns(map: str) -> list[str]:
    lines = get_lines(map)
    lines = [list(line) for line in lines]
    return list(zip(*lines))


def parse_part(part: str):
    columns = get_columns(part)
    return [c.count("#") - 1 for c in columns]


def parse(input: str):
    parts, keys, locks = get_parts(input), [], []
    for p in parts:
        data = parse_part(p)
        locks.append(data) if p.startswith("#") else keys.append(data)
    return keys, locks


def check(lock: list[int], key: list[int]) -> bool:
    sums = [a + b for a, b in zip(lock, key)]
    for s in sums:
        if s > 5:
            return False
    return True


def logic(input: str):
    keys, locks = parse(input)
    sum = 0

    for lock in locks:
        for key in keys:
            sum += check(lock, key)

    return sum


# --- Example ---


def test_example_1():
    example = """
    #####
    .####
    .####
    .####
    .#.#.
    .#...
    .....

    #####
    ##.##
    .#.##
    ...##
    ...#.
    ...#.
    .....

    .....
    #....
    #....
    #...#
    #.#.#
    #.###
    #####

    .....
    .....
    #.#..
    ###..
    ###.#
    ###.#
    #####

    .....
    .....
    .....
    #....
    #.#..
    #.#.#
    #####
    """
    assert logic(example) == 3


# --- Input ---


def test_input():
    result = logic(input)
    assert result == 3317
