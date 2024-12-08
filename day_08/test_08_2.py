import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utilities.maps import (
    M,
    P,
)

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logic ---


def find_reflects(i: int, a: P, b: P, map: M) -> set[P]:
    x, y = (
        b[0] + (b[0] - a[0]) * i,
        b[1] + (b[1] - a[1]) * i,
    )

    if map.out(x, y):
        return set()

    return find_reflects(i + 1, a, b, map).union({(x, y)})


def find_anti_nodes(
    i: int,
    all: list[P],
    map: M,
) -> set[P]:
    if i >= len(all):
        return set()

    a = all[i]
    others = all[:i] + all[i + 1 :]

    antinodes = set()
    for o in others:
        reflects = find_reflects(0, a, o, map)
        antinodes.update(reflects)

    return find_anti_nodes(i + 1, all, map).union(antinodes)


def logic(input: str) -> int:
    map = M(input)
    antennas_by_type = map.list_points()

    antinodes = set()
    for v, antennas in antennas_by_type.items():
        nodes = find_anti_nodes(0, antennas, map)
        antinodes.update(nodes)

    # p = map.merge(antinodes, "#", True)
    # p.print()

    return len(antinodes)


# --- Example ---


def test_example_1():
    example = """
    T.........
    ...T......
    .T........
    ..........
    ..........
    ..........
    ..........
    ..........
    ..........
    ..........

    """
    assert logic(example) == 9


def test_example():
    example = """
    ............
    ........0...
    .....0......
    .......0....
    ....0.......
    ......A.....
    ............
    ............
    ........A...
    .........A..
    ............
    ............
    """
    assert logic(example) == 34


# --- Input ---


def test_input():
    result = logic(input)
    assert result == 1077
