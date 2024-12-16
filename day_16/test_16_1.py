import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities.maps import DP, Dir, M, P, PriorityQueue

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logic ---


class Rein(DP):
    def __init__(self, p: P, dir: Dir, score: int = 0):
        super().__init__(p, dir)
        self.score = score

    def turn_right(self):
        super().turn_right()
        self.score += 1000

    def turn_left(self):
        super().turn_left()
        self.score += 1000

    def move_r(self, dir: Dir) -> "Rein | None":
        r = self.copy()
        match (dir.value - self.dir.value) % 4:
            case 0:
                r.score += 1
            case 1 | 3:
                r.score += 1000 + 1
            case 2:
                return None  # u-turn

        r.move(dir)
        return r

    def copy(self):
        return Rein(self.p, self.dir, self.score)


def explore(map: M, rein: Rein) -> int | None:
    queue = PriorityQueue()
    queue.push((rein.p, rein.dir), (rein, set()), rein.score)
    cache = {}

    while not queue.is_empty():
        result = queue.pop()
        rein, visited = result.item

        key = (rein.p, rein.dir)
        if key in cache and rein.score >= cache[key]:
            continue
        cache[key] = rein.score

        if rein.p in visited:
            continue
        visited.add(rein.p)

        c = map.get(*rein.p)

        if c == "#":
            continue

        if c == "E":
            return rein.score

        for d in Dir:
            next = rein.move_r(d)
            if next is None:
                continue

            queue.push((next.p, next.dir), (next, visited.copy()), next.score)

    return None


def parse_map(input: str):
    map = M(input)
    reindeer = map.find_one("S")
    assert reindeer
    map.remove_item(reindeer)
    return map, Rein(reindeer, Dir.right)


def logic(input: str) -> int | None:
    map, reindeer = parse_map(input)
    return explore(map, reindeer)


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
    assert logic(example) == 7036


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
    assert logic(example) == 11048


# --- Input ---


def test_input():
    result = logic(input)
    assert result == 130536
