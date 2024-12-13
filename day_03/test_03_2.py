import os
import sys
from pathlib import Path

from test_03_1 import calc

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logic ---


def check(scope: str) -> bool | None:
    if scope.startswith("do()"):
        return True

    if scope.startswith("don't()"):
        return False

    return None


def logic(input: str) -> int:
    do = True
    sum = 0
    for i in range(len(input)):
        scope = input[i : i + 12]

        if (action := check(scope)) is not None:
            do = action
            continue

        if not do:
            continue

        sum += calc(scope)

    return sum


# --- Example ---


def test_example():
    example = (
        "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    )
    assert logic(example) == 48


# --- Input ---


def test_input():
    result = logic(input)
    assert result == 80747545
