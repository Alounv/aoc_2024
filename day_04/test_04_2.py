import os
import re
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities.parse import get_diagonals, get_lines

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logic ---


def screen(lines: list[str]):
    found = 0

    for i, line in enumerate(lines):
        matches = list(re.finditer("MAS", line)) + list(re.finditer("SAM", line))

        for match in matches:
            a_index = match.start() + 1

            up_line = lines[i - 2]
            bt_line = lines[i + 2]

            up_offset = (len(up_line) - len(line)) // 2
            bt_offset = (len(bt_line) - len(line)) // 2

            up = up_line[a_index + up_offset]
            bt = bt_line[a_index + bt_offset]

            if {"M", "S"} == {up, bt}:
                found += 1

    return found


def logic(input: str) -> int:
    lines = get_lines(input)
    d1, _ = get_diagonals(lines)

    return screen(d1)

    # --- Example ---


def test_1():
    example = """
    MMSS
    .AA.
    MMSS
    ....
    """
    assert logic(example) == 2


def test_2():
    example = """
    .......
    .......
    ...S.M.
    ....A..
    ...S.M.
    .......
    .......
    """
    assert logic(example) == 1


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
    assert logic(example) == 9


# --- Input ---


def test_input():
    result = logic(input)
    assert result == 1950
