import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from day_22.test_22_1 import next_secret
from utilities.parse import get_lines

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()


def key(diffs: list[int]) -> int:
    hash_val = 17
    for num in diffs:
        hash_val = hash_val * 31 + num
    return hash_val


def compute(secret: int, steps: int, seqs: dict[int, int]):
    prev = secret % 10
    diffs: list[int] = []
    seen = set()

    for _ in range(steps):
        # update secret and get price
        secret = next_secret(secret)
        price = secret % 10

        # compute sequence
        diffs.append(price - prev)
        prev = price
        if len(diffs) < 5:
            continue
        diffs = diffs[1:]

        # increment sequence value if first for this buyer
        k = key(diffs)
        if k in seen:
            continue
        seen.add(k)
        seqs[k] = seqs.get(k, 0) + price


def logic(input: str, steps: int = 2000):
    sequences = {}
    secrets = [int(line) for line in get_lines(input)]
    [compute(s, steps, sequences) for s in secrets]
    return max(sequences.values())


# --- Example ---


def test_example_2():
    example = """
    1
    2
    3
    2024
    """
    assert logic(example) == 23


# --- Input ---


def test_input():
    assert logic(input) == 2044
