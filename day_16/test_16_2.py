import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from day_16.test_16_1 import Rein, explore, parse_map
from utilities.maps import Dir, M, P, PriorityQueue

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logic ---


def backward(map: M, end: P, score: int, seen: dict[tuple[P, Dir], int]) -> set[P]:
    queue = PriorityQueue()
    for d in Dir:
        queue.push(Rein(end, d, score), score)

    visited = set()

    while not queue.is_empty():
        result = queue.pop()
        rein = result.item
        key = (rein.p, rein.dir)

        visited.add(rein.p)

        for d in Dir:
            next = rein.move_back(d)
            if next is None:
                continue

            c = map.get(*next.p)
            if c == "#":
                continue

            key = (next.p, next.dir)
            if key in seen and next.score != seen[key]:
                continue

            queue.push(next, next.score)

    return visited


def logic(input: str) -> int | None:
    map, start, end = parse_map(input)
    score, seen = explore(map, Rein(start, Dir.right))
    best = backward(map, end, score, seen)
    (map.merge(best, "O")).print({"O": 13})
    return len(best)


# --- Example ---


def test_example_1():
    example = """
    ###############
    #.......#....E#
    #.#.###.#.###.#
    #.....#.#...#.#
    #.###.#####.#.#
    #.#.#.......#.#
    #.#.#####.###.#
    #...........#.#
    ###.#.#####.#.#
    #...#.....#.#.#
    #.#.#.###.#.#.#
    #.....#...#.#.#
    #.###.#.#.#.#.#
    #S..#.....#...#
    ###############
    """
    assert logic(example) == 45


def test_example_2():
    example = """
    #################
    #...#...#...#..E#
    #.#.#.#.#.#.#.#.#
    #.#.#.#...#...#.#
    #.#.#.#.###.#.#.#
    #...#.#.#.....#.#
    #.#.#.#.#.#####.#
    #.#...#.#.#.....#
    #.#.#####.#.###.#
    #.#.#.......#...#
    #.#.###.#####.###
    #.#.#...#.....#.#
    #.#.#.#####.###.#
    #.#.#.........#.#
    #.#.#.#########.#
    #S#.............#
    #################
    """
    assert logic(example) == 64


# # # --- Input ---


def test_input():
    result = logic(input)
    assert result == 1024
