import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utilities.maps import (
    DP,
    Dir,
    M,
    P,
)

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logic ---

obstacles = frozenset({"#"})


def move_to_obs(map: M, p: DP, visited: set[P]):
    steps, is_out = map.move_until(p, obstacles)
    visited.update(steps)

    if is_out:
        return True

    p.turn_right()
    return False


def move_until_out(map: M, guard: DP):
    visited = set()

    while True:
        is_out = move_to_obs(map, guard, visited)
        if is_out:
            break

    return visited


def get_guard(map: M) -> DP:
    s = map.find_one("^")
    assert s, "Could not find start position '^' in map"
    return DP(s, Dir.up)


def logic(input: str) -> int:
    map = M(input)
    guard = get_guard(map)
    visited = move_until_out(map, guard)
    # map.merge(visited, "X").print({"#": 13})
    return len(visited)


# --- Example ---


def test_example():
    example = """
    ....#.....
    .........#
    ..........
    ..#.......
    .......#..
    ..........
    .#..^.....
    ........#.
    #.........
    ......#...
    """
    assert logic(example) == 41


# --- Input ---


def test_input():
    result = logic(input)
    assert result == 5101
