import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities.parse import get_lines, get_parts

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logic ---


def parse(input: str):
    parts = get_parts(input)
    r_lines = get_lines(parts[0])
    u_lines = get_lines(parts[1])

    rules = [tuple(map(int, r.split("|"))) for r in r_lines]
    updates = [list(map(int, u.split(","))) for u in u_lines]

    before: dict[int, set[int]] = {}
    after: dict[int, set[int]] = {}
    for b, a in rules:
        before.setdefault(a, set()).add(b)
        after.setdefault(b, set()).add(a)

    return before, after, updates


def check(
    before: dict[int, set[int]], after: dict[int, set[int]], update: list[int]
) -> bool:
    for i, c in enumerate(update):
        if before.get(c, set()).intersection(update[i + 1 :]):
            return False
        if after.get(c, set()).intersection(update[:i]):
            return False

    return True


def get_good_updates(
    before: dict[int, set[int]], after: dict[int, set[int]], updates: list[list[int]]
):
    return list(filter(lambda u: check(before, after, u), updates))


def get_wrong_updates(
    before: dict[int, set[int]], after: dict[int, set[int]], updates: list[list[int]]
):
    return list(filter(lambda u: not check(before, after, u), updates))


def middle(ls: list[int]) -> int:
    return ls[len(ls) // 2]


def logic(input: str) -> int:
    before, after, updates = parse(input)

    filtered_updates = get_good_updates(before, after, updates)
    return sum(map(middle, filtered_updates))


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
    assert logic(example) == 143


# --- Input ---


def test_input():
    result = logic(input)
    assert result == 7024
