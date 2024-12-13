import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities.maps import M, P

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logic ---


def find_paths(map: M, start: P) -> set[P]:
    destinations = set()
    heads: dict[P, str] = {start: "0"}

    while True:
        new_heads: dict[P, str] = dict()

        # for all current head find next possible path
        for h, alt in heads.items():
            if alt == "9":
                destinations.add(h)
                continue

            up = str(int(alt) + 1)
            neighbors = map.get_neighbors(h, up)
            new_heads.update(neighbors)

        # stop if no more heads
        if len(new_heads) == 0:
            break

        # replace heads by next ones
        heads = new_heads

    # print("\n")
    # (map.merge(destinations, "#")).print({"#": 13})
    return destinations


def get_heads(map: M) -> list[P]:
    return map.find_all("0")


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
    ...0...
    ...1...
    ...2...
    6543456
    7.....7
    8.....8
    9.....9
    """
    map = M(example)

    heads = get_heads(map)
    assert heads == [(3, 0)]

    destinations = find_paths(map, (3, 0))

    assert len(destinations) == 2


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
    assert len(destinations) == 5

    assert logic(example) == 36


# --- Input ---


def test_input():
    result = logic(input)
    assert result == 611
