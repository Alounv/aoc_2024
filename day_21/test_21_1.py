import os
import re
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities.maps import M, P
from utilities.parse import get_lines

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()


class Pad:
    def __init__(self, grid: str):
        self.map = M(grid)
        self.paths = self.compute()

    def is_valid(self, dx: int, dy: int, p: P) -> bool:
        x, y = p
        return self.map.get(x + dx, y + dy) != "."

    def compute(self) -> dict[str, set[str]]:
        points = self.map.dict.items()
        paths = {}

        for pa, ca in points:
            for pb, cb in points:
                dx = pb[0] - pa[0]
                dy = pb[1] - pa[1]
                h = ">" * dx if dx > 0 else "<" * -dx
                v = "v" * dy if dy > 0 else "^" * -dy
                key = ca + cb
                paths[key] = set()

                if h + v == "":
                    paths[key].add("A")
                    continue

                if self.is_valid(dx, 0, pa):
                    paths[key].add(h + v + "A")

                if self.is_valid(0, dy, pa):
                    paths[key].add(v + h + "A")

        return paths


# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+

NUMPAD = Pad("""
.....
.789.
.456.
.123.
..0A.
.....
""")


#    +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+

DIRPAD = Pad("""
.....
..^A.
.<v>.
.....
""")


cache = {}


def find(input: str, steps: int, is_first: bool = False) -> int:
    key = input, steps
    if key in cache:
        return cache[key]

    if steps == 0:
        return len(input)

    pair_paths = NUMPAD.paths if is_first else DIRPAD.paths
    input = "A" + input
    sum = 0

    for i in range(len(input) - 1):
        pair = input[i : i + 2]
        paths = pair_paths[pair]
        sum += min(find(p, steps - 1) for p in paths)

    if not is_first:
        cache[key] = sum
    return sum


def num(input: str) -> int:
    numbers = re.sub(r"[^0-9]", "", input)  # removes everything except numbers
    return int(numbers)


def logic(input: str, steps: int) -> int:
    lines = get_lines(input)
    sum = 0

    for line in lines:
        sum += find(line, steps + 1, True) * num(line)

    return sum


# --- Example ---


def test_example():
    example = """
    029A
    980A
    179A
    456A
    379A
    """
    assert logic(example, 2) == 126384


# --- Input ---


def test_input():
    result = logic(input, 2)
    assert result == 152942
