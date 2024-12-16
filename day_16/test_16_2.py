import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from day_16.test_16_1 import Rein, explore, parse_map
from utilities.maps import Dir, M, PriorityQueue

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logic ---


def find_seat(map: M, rein: Rein, best: int) -> int | None:
    cache = {}
    queue = PriorityQueue()
    queue.push((rein.p, rein.dir), (rein, set()), rein.score)
    best_seats = set()

    while not queue.is_empty():
        test = queue.pop()
        rein, visited = test.item

        if rein.score > best:
            continue

        key = (rein.p, rein.dir)
        if key in cache and rein.score > cache[key]:
            continue
        cache[key] = rein.score

        if rein.p in visited:
            continue
        visited.add(rein.p)

        c = map.get(*rein.p)

        if c == "E":
            if rein.score == best:
                best_seats.update(visited)
                continue

        for d in Dir:
            next = rein.move_r(d)
            if next is None:
                continue

            if map.get(*next.p) == "#":
                continue

            queue.push(
                (next.p, next.dir),
                (next, visited.copy()),
                next.score,
            )

    (map.merge(best_seats, "O")).print({"O": 13})
    return len(best_seats)


def logic(input: str) -> int | None:
    map, reindeer = parse_map(input)
    score = explore(map, reindeer)
    assert score
    return find_seat(map, reindeer, score)


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
