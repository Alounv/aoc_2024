from enum import Enum

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


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


class DirPoint:
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
        return Point(self.x, self.y)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.dir.value})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.dir == other.dir

    def __hash__(self):
        return hash((self.x, self.y, self.dir.value))

    def copy(self):
        return DirPoint(self.x, self.y, self.dir)


def get_map(raw: str, ignore=".") -> dict[tuple[int, int], str]:
    result = {}
    for y, line in enumerate(get_lines(raw)):
        for x, c in enumerate(line):
            if c == ignore:
                continue
            result[x, y] = c
    return result


class MyMap:
    def __init__(self, input: str):
        lines = get_lines(input)

        self.height = len(lines)
        self.width = len(lines[0])
        self.map = get_map(input)

    def get(self, x, y) -> str:
        return self.map.get((x, y), ".")

    def check(self, x, y, chars: set[str]) -> bool:
        return self.map.get((x, y), None) in chars

    def set(self, x, y, value: str):
        self.map[x, y] = value

    def out(self, x: int, y: int) -> bool:
        return x < 0 or y < 0 or x >= self.width or y >= self.height

    def find_one(self, char: str) -> tuple[int, int] | None:
        return next((p for p, c in self.map.items() if c == char), None)

    def get_lines(self) -> list[str]:
        lines = []
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                line += self.map.get((x, y), ".")
            lines.append(line)
        return lines

    def __str__(self):
        return "\n".join(self.get_lines())

    def copy(self):
        map_copy = MyMap.__new__(MyMap)
        map_copy.height = self.height
        map_copy.width = self.width
        map_copy.map = self.map.copy()
        return map_copy
