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

DELTAS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
EMPTY = "."


def get_neighbors(p: P) -> list[P]:
    n: list[P] = []
    for dx, dy in DELTAS:
        x = p[0] + dx
        y = p[1] + dy
        n.append((x, y))
    return n


class DP:
    def __init__(self, p: P, dir: Dir):
        self.p = p
        self.dir = dir

    def turn_right(self):
        self.dir = self.dir.rotate_right()

    def turn_left(self):
        self.dir = self.dir.rotate_left()

    def __str__(self):
        return f"({self.p}, {self.dir})"

    def __eq__(self, other):
        return self.p == other.p and self.dir == other.dir

    def __hash__(self):
        return hash((self.p, self.dir.value))

    def copy(self):
        return DP(self.p, self.dir)


class M:
    def __init__(self, input: str):
        lines = get_lines(input)
        self.height = len(lines)
        self.width = len(lines[0])

        self.dict: dict[P, str] = {}
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == EMPTY:
                    continue
                self.dict[x, y] = c

    @classmethod
    def empty(cls, width: int, height: int) -> "M":
        m = cls.__new__(cls)
        m.height = height
        m.width = width
        m.dict = {}
        return m

    def get(self, x, y) -> str:
        return self.dict.get((x, y)) or EMPTY

    def set_item(self, p: P, value: str):
        self.dict[p] = value

    def remove_item(self, p: P):
        del self.dict[p]

    def switch(self, a: P, b: P):
        dict = self.dict
        a_exists = a in dict
        b_exists = b in dict

        if a_exists and b_exists:
            dict[a], dict[b] = dict[b], dict[a]
        elif a_exists and not b_exists:
            v = dict[a]
            dict[b] = v
            del dict[a]
        elif b_exists and not a_exists:
            v = dict[b]
            dict[a] = v
            del dict[b]

    def set_if_empty(self, p: P, value: str):
        x, y = p
        if self.get(x, y) == EMPTY:
            self.dict[p] = value

    def list_points(self) -> dict[str, list[P]]:
        result = {}
        for x, y in self.dict.keys():
            v = self.get(x, y)
            result.setdefault(v, []).append((x, y))

        return result

    def merge(self, points: set[P], value: str, down: bool = False):
        result = self.copy()
        for p in points:
            if down:
                result.set_if_empty(p, value)
            else:
                result.set_item(p, value)
        return result

    def out(self, x: int, y: int) -> bool:
        return x < 0 or y < 0 or x >= self.width or y >= self.height

    def move_until(self, dp: DP, obs: frozenset[str]) -> tuple[set[P], bool]:
        dx, dy = DELTAS[dp.dir.value]
        steps = {dp.p}

        while True:
            x, y = dp.p
            next = (x + dx, y + dy)

            if self.out(*next):
                return steps, True

            if self.get(*next) in obs:
                return steps, False

            steps.add(next)
            dp.p = next

    def find_one(self, char: str) -> P | None:
        return next((p for p, c in self.dict.items() if c == char), None)

    def find_all(self, char: str) -> list[P]:
        return [p for p, c in self.dict.items() if c == char]

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
                line += self.get(x, y)
            lines.append(line)
        return lines

    def __str__(self):
        return "\n".join(self.get_lines())

    def print(self, colors: dict[str, int] = {}, clean: bool = False):
        if clean:
            print("\033[2J\033[H", end="")
        else:
            print("\n")

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
        m.dict = self.dict.copy()
        return m
