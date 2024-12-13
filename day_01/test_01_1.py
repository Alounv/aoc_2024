import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities.parse import get_lines

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logic ---


def get_two_lists(input: str) -> tuple[list, list]:
    list_1, list_2 = [], []

    for line in get_lines(input):
        num1, num2 = map(int, line.split())
        list_1.append(num1)
        list_2.append(num2)

    return list_1, list_2


def logic(input: str) -> int:
    # Get two lists of numbers
    list_1, list_2 = get_two_lists(input)

    # Sort both lists
    list_1.sort()
    list_2.sort()

    # Calculate sum of absolute differences between each pair of numbers
    return sum(abs(a - b) for a, b in zip(list_1, list_2))


# --- Example ---


def test_example():
    example = """
    3   4
    4   3
    2   5
    1   3
    3   9
    3   3
    """
    assert logic(example) == 11


# --- Input ---


def test_input():
    result = logic(input)
    assert result == 2113135
