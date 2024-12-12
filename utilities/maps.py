from enum import Enum

from utilities.colors import color
from utilities.parse import get_lines


class Dir(Enum):
    up = 0
    right = 1
    down = 2
    left = 3

    def __hash__(self):
        return self.value

    def rotate_left(self):
        return Dir((self.value - 1) % 4)

    def rotate_right(self):
        return Dir((self.value + 1) % 4)

    def __str__(self):
        match self:
            case Dir.up:
                return "^"
            case Dir.right:
                return ">"
            case Dir.down:
                return "v"
            case Dir.left:
                return "<"


P = tuple[int, int]

deltas = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def get_neighbors(p: P) -> list[P]:
    n: list[P] = []
    for dx, dy in deltas:
        x = p[0] + dx
        y = p[1] + dy
        n.append((x, y))
    return n


class DP:
    def __init__(self, x: int, y: int, dir: Dir):
        self.x = x
        self.y = y
        self.dir = dir

    def next(self):
        next = self.copy()
        match self.dir:
            case Dir.up:
                next.y -= 1
            case Dir.right:
                next.x += 1
            case Dir.down:
                next.y += 1
            case Dir.left:
                next.x -= 1

        return next

    def turn_right(self):
        self.dir = self.dir.rotate_right()

    def turn_left(self):
        self.dir = self.dir.rotate_left()

    def point(self):
        return (self.x, self.y)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.dir.value})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.dir == other.dir

    def __hash__(self):
        return hash((self.x, self.y, self.dir.value))

    def copy(self):
        return DP(self.x, self.y, self.dir)


class M:
    def __init__(self, input: str, empty="."):
        lines = get_lines(input)
        self.height = len(lines)
        self.width = len(lines[0])
        self.empty = empty

        self.map = {}
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == empty:
                    continue
                self.map[x, y] = c

    def get(self, x, y) -> str:
        return self.map.get((x, y), self.empty)

    def check(self, x, y, chars: set[str]) -> bool:
        return self.map.get((x, y), None) in chars

    def list_points(self) -> dict[str, list[P]]:
        result = {}
        for x, y in self.map.keys():
            v = self.get(x, y)
            result.setdefault(v, []).append((x, y))

        return result

    def merge(self, points: set[P], value: str, down: bool = False):
        result = self.copy()
        for p in points:
            if down:
                result.map[p] = result.map.get(p, value)
            else:
                result.map[p] = value
        return result

    def set(self, p: P, value: str):
        self.map[p] = value

    def out(self, x: int, y: int) -> bool:
        return x < 0 or y < 0 or x >= self.width or y >= self.height

    def find_one(self, char: str) -> P | None:
        return next((p for p, c in self.map.items() if c == char), None)

    def find_all(self, char: str) -> list[P]:
        return [p for p, c in self.map.items() if c == char]

    def get_neighbors(self, p: P, value: str | None = None) -> dict[P, str]:
        n: dict[P, str] = {}
        for x, y in get_neighbors(p):
            if self.out(x, y):
                continue

            v = self.get(x, y)

            if value and v != value:
                continue

            n[(x, y)] = v
        return n

    def get_lines(self) -> list[str]:
        lines = []
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                line += self.map.get((x, y), self.empty)
            lines.append(line)
        return lines

    def __str__(self):
        return "\n".join(self.get_lines())

    def print(self, colors: dict[str, int] | None = None):
        print("\n")

        if colors is None:
            print(str(self))
        else:
            spec = {
                ".": 0,
                "1": 1,
                "2": 2,
                "3": 3,
                "4": 4,
                "5": 5,
                "6": 6,
                "7": 7,
                "8": 8,
                "9": 9,
                "0": 10,
                "#": 11,
            }
            spec.update(colors)
            print(color(str(self), spec))

    def copy(self):
        m = M.__new__(M)
        m.height = self.height
        m.width = self.width
        m.map = self.map.copy()
        m.empty = self.empty
        return m
