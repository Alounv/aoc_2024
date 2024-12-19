import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities.parse import get_parts

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logc ---


def parse(input: str) -> tuple[set[str], list[str]]:
    towels, patterns = get_parts(input)
    towels = set([t.strip() for t in towels.split(", ")])
    patterns = [p.strip() for p in patterns.split("\n")]
    return towels, patterns


def check(towels: set[str], pattern: str, cache: dict[str, bool]) -> bool:
    if not pattern:
        return True

    if pattern in cache:
        return cache[pattern]

    matches = False
    for t in towels:
        if pattern.startswith(t):
            if check(towels, pattern[len(t) :], cache):
                matches = True
                break

    cache[pattern] = matches
    return matches


def logic(input: str) -> int:
    towels, patterns = parse(input)

    sum = 0
    cache = {}
    for p in patterns:
        result = check(towels, p, cache)
        sum += int(result)

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

    assert logic(example) == 6


# --- Input ---


def test_input_1():
    pattern = "uubwgrrrwggwwgwbbwuwgwguurggurrrugbggguwbggbggbuuwg"
    towels, _ = parse(input)
    assert check(towels, pattern, {})


def test_input_2():
    pattern = "uwgbwwgwwgwrwwbrruubuugrgrrwbwburgbguuugwrwwgrbbubwwgrbb"
    towels, _ = parse(input)
    assert not check(towels, pattern, {})


def test_input():
    result = logic(input)

    assert result == 353
