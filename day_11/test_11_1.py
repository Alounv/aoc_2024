import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities.parse import get_lines

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logic ---


def split(num: str) -> tuple[int, int]:
    size = len(num) // 2
    a = int(num[:size])
    b = int(num[size:])
    return a, b


def count(num: int, i: int, cache: dict[tuple[int, int], int] = {}) -> int:
    if i == 0:
        return 1

    key = (num, i)
    if key in cache:
        return cache[key]

    i = i - 1

    if num == 0:
        result = count(1, i)
    else:
        str_num = str(num)
        size = len(str_num)
        if size % 2 == 0:
            a, b = split(str_num)
            result = count(a, i) + count(b, i)
        else:
            result = count(num * 2024, i)

    cache[key] = result
    return result


def logic(input: str, steps: int) -> int:
    lines = get_lines(input)
    words = lines[0].split(" ")
    nums = [int(word) for word in words]

    sum = 0
    for num in nums:
        sum += count(num, steps)

    return sum


# --- Example ---


def test_example_1():
    assert count(0, 1) == 1
    assert count(0, 2) == 1
    assert count(0, 3) == 2
    assert count(0, 4) == 4


def test_example_2():
    example = "0 1 10 99 999"
    assert logic(example, 1) == 7


def test_example_3():
    example = "125 17"
    assert logic(example, 25) == 55312


# --- Input ---


def test_part_1():
    result = logic(input, 25)
    assert result == 185205
