import os
import re
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities.parse import get_columns, get_diagonals, get_lines

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logic ---


def screen(lines: list[str], search: str) -> int:
    sum = 0
    reverse = search[::-1]

    for line in lines:
        matches = len(re.findall(search, line))
        matches += len(re.findall(reverse, line))
        sum += matches

    return sum


def logic(input: str) -> int:
    lines = get_lines(input)
    columns = get_columns(lines)
    d1, d2 = get_diagonals(lines)

    all = lines + columns + d1 + d2

    return screen(all, "XMAS")


# --- Example ---


def test_example():
    example = """
    MMMSXXMASM
    MSAMXMSMSA
    AMXSXMAAMM
    MSAMASMSMX
    XMASAMXAMM
    XXAMMXXAMA
    SMSMSASXSS
    SAXAMASAAA
    MAMMMXMMMM
    MXMXAXMASX
    """
    assert logic(example) == 18


# --- Input ---


def test_input():
    result = logic(input)
    assert result == 2593
