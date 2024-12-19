import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from day_19.test_19_1 import parse

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logc ---


def check(towels: set[str], pattern: str, cache: dict[str, int]) -> int:
    if not pattern:
        return 1

    if pattern in cache:
        return cache[pattern]

    matches = 0
    for t in towels:
        if pattern.startswith(t):
            matches += check(towels, pattern[len(t) :], cache)

    cache[pattern] = matches
    return matches


def logic(input: str) -> int:
    towels, patterns = parse(input)

    sum = 0
    cache = {}
    for p in patterns:
        sum += check(towels, p, cache)

    return sum


# --- Example ---


def test_example_1():
    example = """
    r, wr, b, g, bwu, rb, gb, br

    brwrr
    bggr
    gbbr
    rrbgbr
    ubwu
    bwurrg
    brgr
    bbrgwb
    """

    assert logic(example) == 16


# --- Input ---


def test_input():
    result = logic(input)
    assert result == 880877787214477
