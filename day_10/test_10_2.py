import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from day_10.test_10_1 import get_heads
from utilities.maps import M, P

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logic ---


def find_paths(map: M, start: P) -> list[P]:
    destinations = []
    heads: list[tuple[P, str]] = [(start, "0")]

    while True:
        new_heads: list[tuple[P, str]] = []

        # for all current head find next possible path
        for h, alt in heads:
            if alt == "9":
                destinations.append(h)
                continue

            up = str(int(alt) + 1)
            neighbors = map.get_neighbors(h, up)
            new_heads.extend(list(neighbors.items()))

        # stop if no more heads
        if len(new_heads) == 0:
            break

        # replace heads by next ones
        heads = new_heads

    # print("\n")
    # (map.merge(destinations, "#")).print({"#": 13})
    return destinations


def logic(input: str) -> int:
    m = M(input)
    heads = get_heads(m)

    sum = 0
    for h in heads:
        destinations = find_paths(m, h)
        sum += len(destinations)
    return sum


# --- Example ---


def test_example_1():
    example = """
    .....0.
    ..4321.
    ..5..2.
    ..6543.
    ..7..4.
    ..8765.
    ..9....
    """
    map = M(example)

    heads = get_heads(map)
    assert heads == [(5, 0)]

    destinations = find_paths(map, (5, 0))
    assert len(destinations) == 3


def test_example_2():
    example = """
    89010123
    78121874
    87430965
    96549874
    45678903
    32019012
    01329801
    10456732
    """
    map = M(example)

    heads = get_heads(map)
    assert heads == [
        (2, 0),
        (4, 0),
        (4, 2),
        (6, 4),
        (2, 5),
        (5, 5),
        (0, 6),
        (6, 6),
        (1, 7),
    ]

    destinations = find_paths(map, (2, 0))
    assert len(destinations) == 20

    assert logic(example) == 81


# # --- Input ---


def test_input():
    result = logic(input)
    assert result == 1380
