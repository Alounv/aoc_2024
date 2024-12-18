import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities.maps import M, P, PriorityQueue
from utilities.parse import get_lines

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logc ---


def parse(input: str) -> list[P]:
    lines = get_lines(input)

    bytes: list[P] = []
    for line in lines:
        x, y = map(int, line.split(","))
        bytes.append((x, y))
    return bytes


def find(map: M, p: P, visited: set[P], steps: int, target: P) -> int | None:
    queue = PriorityQueue()
    queue.push(p, steps)

    while not queue.is_empty():
        r = queue.pop()
        p = r.item
        steps = r.priority

        if p in visited:
            continue
        visited.add(p)

        if p == (target or map.end()):
            return steps

        for n in map.get_neighbors(p, "."):
            queue.push(n, steps + 1)

    return None


def logic(input: str, dim: int, limit: int) -> int | None:
    bytes = parse(input)
    bytes = bytes[:limit]
    map = M.empty(dim, dim).merge(set(bytes), "#")
    return find(map, (0, 0), set(), 0, map.end())


# --- Example ---


def test_example_1():
    example = """
    5,4
    4,2
    4,5
    3,0
    2,1
    6,3
    2,4
    1,5
    0,6
    3,3
    2,6
    5,1
    1,2
    5,5
    2,5
    6,5
    1,4
    0,4
    6,4
    1,1
    6,1
    1,0
    0,5
    1,6
    2,0
    """

    assert logic(example, 7, 12) == 22


# --- Input ---


def test_input():
    result = logic(input, 71, 1024)

    assert result == 308
