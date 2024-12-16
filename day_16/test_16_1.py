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

    def move_r(self, dir: Dir) -> "Rein | None":
        r = self.copy()
        match (dir.value - self.dir.value) % 4:
            case 0:
                r.score += 1
                r.move(dir)
                return r
            case 1:
                r.score += 1000
                r.turn_right()
            case 2:
                return None  # u-turn
            case 3:
                r.score += 1000
                r.turn_left()

        return r

    def move_back(self, dir: Dir) -> "Rein | None":
        r = self.copy()
        match (dir.value - self.dir.value) % 4:
            case 0:
                return None  # u-turn
            case 1:
                r.score -= 1000
                r.turn_right()
            case 2:
                r.score -= 1
                r.move(dir)
            case 3:
                r.score -= 1000
                r.turn_left()

        r.dir = Dir((dir.value + 2) % 4)
        return r

    def copy(self):
        return Rein(self.p, self.dir, self.score)


def explore(map: M, rein: Rein) -> tuple[int, dict[tuple[P, Dir], int]]:
    queue = PriorityQueue()
    queue.push(rein, rein.score)
    seen = {}
    score = 1_000_000_000

    while not queue.is_empty():
        result = queue.pop()
        rein = result.item

        key = (rein.p, rein.dir)
        if key in seen and rein.score >= seen[key]:
            continue

        c = map.get(*rein.p)

        if c == "#":
            continue

        if c == "E":
            score = min(score, rein.score)

        seen[key] = rein.score

        for d in Dir:
            next = rein.move_r(d)
            if next is None:
                continue

            queue.push(next, next.score)

    return score, seen


def parse_map(input: str):
    map = M(input)
    start = map.find_one("S")
    end = map.find_one("E")
    assert start and end
    return map, start, end


def logic(input: str) -> int | None:
    map, start, _ = parse_map(input)
    score, visited = explore(map, Rein(start, Dir.right))
    return score


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
