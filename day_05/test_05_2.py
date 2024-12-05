import os
import sys
from functools import cmp_to_key
from pathlib import Path

from test_05_1 import get_wrong_updates, middle, parse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logic ---


def fix(
    before: dict[int, set[int]], after: dict[int, set[int]], update: list[int]
) -> list[int]:
    def compare(a: int, b: int) -> int:
        if {a}.issubset(before.get(b, set())):
            return -1
        elif {b}.issubset(after.get(a, set())):
            return 1
        return 0

    return sorted(update, key=cmp_to_key(compare))


def logic(input: str) -> int:
    before, after, updates = parse(input)

    wrong = get_wrong_updates(before, after, updates)
    fixed = list(map(lambda u: fix(before, after, u), wrong))

    return sum(map(middle, fixed))


# --- Example ---


def test_example():
    example = """
    47|53
    97|13
    97|61
    97|47
    75|29
    61|13
    75|53
    29|13
    97|29
    53|29
    61|53
    97|53
    61|29
    47|13
    75|47
    97|75
    47|61
    75|61
    47|29
    75|13
    53|13

    75,47,61,53,29
    97,61,53,29,13
    75,29,13
    75,97,47,61,53
    61,13,29
    97,13,75,29,47
    """

    assert logic(example) == 123


# --- Input ---


def test_input():
    result = logic(input)
    assert result == 4151
