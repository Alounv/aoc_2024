import os
import sys
from pathlib import Path

from test_06_1 import get_guard, move_until_out

from utilities.maps import DP, M

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logic ---

obstacles = frozenset({"#", "O"})


def has_loop(args: tuple[M, DP]) -> bool:
    (map, guard) = args
    visited = set({guard.copy()})

    while True:
        _, is_out = map.move_until(guard, obstacles)
        if is_out:
            return False

        guard.turn_right()
        if guard in visited:
            return True

        visited.add(guard.copy())


def logic(input: str) -> int:
    map = M(input)
    guard = get_guard(map)
    visited = move_until_out(map, guard.copy())

    args: list[tuple[M, DP]] = []
    for p in visited:
        m = map.copy()
        m.set_item(p, "O")
        args.append((m, guard.copy()))

    results = [has_loop(arg) for arg in args]

    return sum(results)


# --- Example ---


def test_has_loop():
    example = """
    ....#.....
    ....+---+#
    ....|...|.
    ..#.|...|.
    ..+-+-+#|.
    ..|.|.|.|.
    .#+-^-+-+.
    .+----++#.
    #+----++..
    ......#O..
    """
    map = M(example)
    guard = get_guard(map)
    assert has_loop((map, guard))


def test_has_loop_2():
    example = """
    ....#.....
    .........#
    ..........
    ..#.......
    .......#..
    ..........
    .#..^.....
    ........#.
    #O........
    ......#...
    """
    map = M(example)
    guard = get_guard(map)
    assert has_loop((map, guard))


def test_has_loop_3():
    example = """
    ....#.....
    .........#
    ..........
    ..#.......
    .......#..
    ..........
    .#..^.....
    ..O.....#.
    #.........
    ......#...
     """
    map = M(example)
    guard = get_guard(map)
    assert not has_loop((map, guard))


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
    assert logic(example) == 6


# --- Input ---


def test_input():
    result = logic(input)
    assert result == 1951
