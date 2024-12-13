import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_02_1 import isSafe

from utilities.parse import get_lines

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logic ---


def isSafeWithChange(report: list[int]) -> bool:
    if isSafe(report):
        return True

    return any(isSafe(report[:i] + report[i + 1 :]) for i in range(len(report)))


def logic(input: str) -> int:
    lines = get_lines(input)
    reports = [list(map(int, line.split())) for line in lines]
    safeReports = [report for report in reports if isSafeWithChange(report)]
    return len(safeReports)


# --- Example ---


def test_example():
    example = [1, 2, 3, 4, 2]
    assert isSafe(example) == 0
    assert isSafeWithChange(example) == 1

    example = """
    7 6 4 2 1
    1 2 7 8 9
    9 7 6 2 1
    1 3 2 4 5
    8 6 4 4 1
    1 3 6 7 9
    """
    assert logic(example) == 4


# --- Input ---


def test_input():
    result = logic(input)
    assert result == 476
