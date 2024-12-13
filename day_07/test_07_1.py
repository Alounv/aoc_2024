import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utilities.parse import get_lines

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logic ---


class Eq:
    def __init__(self, input: str):
        result, operands = input.split(": ")
        operands = operands.split(" ")
        self.result = int(result)
        self.operands = [int(x) for x in operands]

    def __str__(self):
        operands = " ".join(map(str, self.operands))
        return f"{self.result}: {operands}"


def parse(input: str) -> list[Eq]:
    lines = get_lines(input)
    return [Eq(line) for line in lines]


def solve(eq: Eq, result: int, i: int) -> bool:
    if result > eq.result:
        return False

    if i == len(eq.operands):
        return result == eq.result

    r1 = solve(eq, result + eq.operands[i], i + 1)
    r2 = solve(eq, result * eq.operands[i], i + 1)

    return r1 or r2


def logic(input: str) -> int:
    equ = parse(input)
    sum = 0

    for e in equ:
        if solve(e, 0, 0):
            sum += e.result

    return sum


# --- Example ---


def test_example():
    example = """
    190: 10 19
    3267: 81 40 27
    83: 17 5
    156: 15 6
    7290: 6 8 6 15
    161011: 16 10 13
    192: 17 8 14
    21037: 9 7 18 13
    292: 11 6 16 20
    """
    assert logic(example) == 3749


# --- Input ---


def test_input():
    result = logic(input)
    assert result == 4364915411363
