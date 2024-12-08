import os
import sys
from multiprocessing import Pool
from pathlib import Path

from test_06_1 import get_guard, move_until_out

from utilities.maps import DP, M

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logic ---


def move_to_obs(map: M, p: DP):
    is_out = False

    while True:
        next = p.next()

        if map.out(next.x, next.y):
            is_out = True
            break

        if map.check(next.x, next.y, {"#", "O"}):
            p.turn_right()
            break

        p = next

    return p, is_out


def has_loop(args: tuple[M, DP]) -> bool:
    (map, guard) = args
    visited = set({guard})

    def check(guard: DP) -> bool:
        next, is_out = move_to_obs(map, guard)
        if is_out:
            return False

        if next in visited:
            return True

        visited.add(next.copy())
        return check(next)

    return check(guard)


def logic(input: str) -> int:
    map = M(input)
    guard = get_guard(map)

    visited = move_until_out(map, guard.copy())

    # for each position try to set an obstacle
    args: list[tuple[M, DP]] = []
    for p in visited:
        m = map.copy()
        m.set(p, "O")
        args.append((m, guard.copy()))

    # this can be parallelize
    with Pool() as pool:
        results = pool.map(has_loop, args)

    # count True results
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
