import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logic ---


def calc(scope: str) -> int:
    if scope[:4] != "mul(":
        return 0

    end = scope[4:12].find(")")
    if end == -1:
        return 0

    inner = scope[4 : 4 + end]
    try:
        n1, n2 = map(int, inner.split(","))
        return n1 * n2
    except ValueError:
        return 0


def logic(input: str) -> int:
    sum = 0
    for i in range(len(input)):
        sum += calc(input[i : i + 12])

    return sum


# --- Example ---


def test_example():
    example = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    assert logic(example) == 161


# --- Input ---


def test_input():
    result = logic(input)
    assert result == 182619815
