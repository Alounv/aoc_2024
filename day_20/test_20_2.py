import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from day_20.test_20_1 import count_savings, get_path, logic, parse

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()


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

    assert count_savings(map, path, 77, 20) == 0
    assert count_savings(map, path, 76, 20) == 3
    assert count_savings(map, path, 75, 20) == 3
    assert count_savings(map, path, 74, 20) == 4 + 3
    assert count_savings(map, path, 73, 20) == 4 + 3
    assert count_savings(map, path, 72, 20) == 22 + 7
    assert count_savings(map, path, 70, 20) == 12 + 29
    assert count_savings(map, path, 68, 20) == 14 + 41
    assert count_savings(map, path, 66, 20) == 12 + 55
    assert count_savings(map, path, 64, 20) == 19 + 67
    assert count_savings(map, path, 62, 20) == 20 + 86
    assert count_savings(map, path, 60, 20) == 23 + 106
    assert count_savings(map, path, 58, 20) == 25 + 129
    assert count_savings(map, path, 56, 20) == 39 + 154
    assert count_savings(map, path, 54, 20) == 29 + 193
    assert count_savings(map, path, 52, 20) == 31 + 222
    assert count_savings(map, path, 50, 20) == 32 + 253


# --- Input ---


def test_input():
    result = logic(input, 100, 20)
    assert result == 1007186
