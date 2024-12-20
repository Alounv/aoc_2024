import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities.maps import M, P

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logc ---


def parse(input: str) -> tuple[M, P, P]:
    map = M(input)
    start = map.find_one("S")
    end = map.find_one("E")
    assert start
    assert end
    map.remove_item(start)
    map.remove_item(end)
    return map, start, end


def get_path(map: M, start: P, end: P) -> dict[P, int]:
    t = 0
    p = start
    path = {p: t}
    prev = p

    while p != end:
        neighbors = map.get_neighbors(p, ".")
        n = next((n for n in neighbors if n != prev), None)
        assert n
        t += 1
        path[n] = t
        prev, p = p, n

    return path


def count_savings(map: M, path: dict[P, int], target: int, max_depth: int) -> int:
    count = 0

    for a, start in path.items():
        for b, end in path.items():
            cheat = abs(a[0] - b[0]) + abs(a[1] - b[1])
            if cheat > max_depth:
                continue

            if end - (start + cheat) >= target:
                count += 1

    return count


def logic(input: str, target: int, max_depth: int) -> int:
    map, start, end = parse(input)
    path = get_path(map, start, end)
    return count_savings(map, path, target, max_depth)


# --- Example ---


def test_example():
    example = """
    ###############
    #...#...#.....#
    #.#.#.#.#.###.#
    #S#...#.#.#...#
    #######.#.#.###
    #######.#.#...#
    #######.#.###.#
    ###..E#...#...#
    ###.#######.###
    #...###...#...#
    #.#####.#.###.#
    #.#...#.#.#...#
    #.#.#.#.#.#.###
    #...#...#...###
    ###############
    """

    map, start, end = parse(example)
    path = get_path(map, start, end)

    # assert count_savings_for_pos(map, path, (7, 6), 64, 2) == 0
    # assert count_savings_for_pos(map, path, (7, 7), 64, 2) == 1
    # assert count_savings_for_pos(map, path, (7, 7), 65, 2) == 0

    assert count_savings(map, path, 65, 2) == 0
    assert count_savings(map, path, 64, 2) == 1
    assert count_savings(map, path, 41, 2) == 1
    assert count_savings(map, path, 40, 2) == 2
    assert count_savings(map, path, 2, 2) == 14 + 14 + 2 + 4 + 2 + 3 + 1 + 1 + 1 + 1 + 1


# --- Input ---


def test_input():
    result = logic(input, 100, 2)
    assert result == 1363
