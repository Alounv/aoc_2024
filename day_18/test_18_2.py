import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from day_18.test_18_1 import find, parse
from utilities.maps import M, P

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logc ---


def get_restart(map: M, p: P, visited: set[P]) -> P | None:
    return next((n for n in map.get_neighbors(p, ".") if n in visited), None)


def logic(input: str, dim: int, limit: int) -> P | None:
    bytes = parse(input)
    map = M.empty(dim, dim).merge(set(bytes), "#")
    visited = set()

    for i in range(len(bytes) - 1, 0, -1):
        p = bytes[i]
        map.remove_item(p)

        # check if we can restart (if so remove it from visited)
        r = map.end() if not len(visited) else get_restart(map, p, visited)
        if r is None:
            continue
        if r in visited:
            visited.remove(r)

        if find(map, r, visited, 0, (0, 0)) is not None:
            return bytes[i]

    return None


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

    assert logic(example, 7, 12) == (6, 1)


# --- Input ---


def test_input():
    result = logic(input, 71, 1024)

    assert result == (46, 28)
