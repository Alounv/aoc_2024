import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_01_1 import get_two_lists

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logic ---


def logic(input: str) -> int:
    # Get two lists of numbers
    list_1, list_2 = get_two_lists(input)

    # Get frequency of each value in list 2
    list_2_freq = {}
    for value in list_2:
        list_2_freq[value] = list_2_freq.get(value, 0) + 1

    # Calculate total sum of each value multiplied by its frequency
    return sum(value * list_2_freq.get(value, 0) for value in list_1)


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
    assert logic(example) == 31


# --- Input ---


def test_input():
    result = logic(input)
    assert result == 19097157
