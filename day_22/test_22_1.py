import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities.parse import get_lines

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# value = s * (2**6)
# s = value ^ s
# s = s % 2**24

# value = s // (2**5)
# s = value ^ s
# s = s % 2**24

# value = s * (2**11)
# s = value ^ s
# s = s % (2**24)


def next_secret(s: int) -> int:
    s = (s * 2**6 ^ s) % 2**24
    s = (s // 2**5 ^ s) % 2**24
    s = (s * 2**11 ^ s) % (2**24)
    return s


def solve(s: int, steps: int) -> int:
    for _ in range(steps):
        s = next_secret(s)
    return s


def logic(input: str, steps: int):
    secrets = [int(line) for line in get_lines(input)]
    return sum([solve(s, steps) for s in secrets])


# --- Example ---


def test_example_1():
    example = """
    123
    """
    assert logic(example, 1) == 15887950
    assert logic(example, 10) == 5908254


def test_example_2():
    example = """
    1
    10
    100
    2024
    """
    assert logic(example, 2000) == 37327623


# --- Input ---


def test_input():
    result = logic(input, 2000)
    assert result == 18261820068
