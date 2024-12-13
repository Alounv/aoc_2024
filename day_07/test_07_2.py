import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from day_07.test_07_1 import Eq, parse

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logic ---


def solve(eq: Eq, result: int = 0, i: int = 0) -> bool:
    if result > eq.result:
        return False

    if i == len(eq.operands):
        return result == eq.result

    r1 = solve(eq, result + eq.operands[i], i + 1)
    r2 = solve(eq, result * eq.operands[i], i + 1)
    r3 = solve(eq, int(str(result) + str(eq.operands[i])), i + 1)

    return r1 or r2 or r3


def logic(input: str) -> int:
    equ = parse(input)

    sum = 0
    for e in equ:
        if solve(e):
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
    assert logic(example) == 11387


# --- Input ---


def test_input():
    result = logic(input)
    assert result == 38322057216320
