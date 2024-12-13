import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities.parse import get_lines

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logic ---


def isSafe(report: list[int]) -> bool:
    dir: str | None = None

    for i in range(1, len(report)):
        # is evolution in the range of 1-3?
        diff = report[i] - report[i - 1]
        if abs(diff) < 1 or abs(diff) > 3:
            return False

        # has changed direction?
        currentDir = "up" if diff > 0 else "down"
        if dir is not None and dir != currentDir:
            return False

        dir = currentDir

    return True


def logic(input: str) -> int:
    lines = get_lines(input)
    reports = [list(map(int, line.split())) for line in lines]
    safeReports = [report for report in reports if isSafe(report)]
    return len(safeReports)


# --- Example ---


def test_example():
    example = """
    7 6 4 2 1
    1 2 7 8 9
    9 7 6 2 1
    1 3 2 4 5
    8 6 4 4 1
    1 3 6 7 9
    """
    assert logic(example) == 2


# --- Input ---


def test_input():
    result = logic(input)
    assert result == 421
