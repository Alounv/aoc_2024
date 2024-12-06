import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utilities.maps import (
    Dir,
    DirPoint,
    MyMap,
)

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logic ---


def move_to_obs(map: MyMap, p: DirPoint):
    is_out = False
    visited = set({p.point()})

    while True:
        next = p.next()

        if map.out(next.x, next.y):
            is_out = True
            break

        if map.check(next.x, next.y, {"#"}):
            p.turn_right()
            visited.add(p.point())
            break

        p = next
        visited.add(p.point())

    return visited, p, is_out


def move_until_out(map: MyMap, guard: DirPoint):
    visited = set({guard.point()})

    while True:
        new, guard, is_out = move_to_obs(map, guard)
        visited = visited.union(new)
        if is_out:
            break

    return visited


def get_guard(map: MyMap) -> DirPoint:
    s = map.find_one("^")
    assert s, "Could not find start position '^' in map"
    x, y = s
    return DirPoint(x, y, Dir.up)


def logic(input: str) -> int:
    map = MyMap(input)
    guard = get_guard(map)
    visited = move_until_out(map, guard)
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


# def test_input():
#     result = logic(input)
#     assert result == 5101
