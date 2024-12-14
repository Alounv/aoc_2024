import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities.maps import M, P
from utilities.parse import get_lines

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logic ---


class Robot:
    def __init__(self, p: P, v: P, max_x: int, max_y: int):
        self.p = p
        self.v = v
        self.max_x = max_x
        self.max_y = max_y

    def __str__(self):
        return f"P: {self.p}\nV: {self.v}"

    def move(self, dt: int):
        x, y = self.p
        vx, vy = self.v

        x += vx * dt
        y += vy * dt

        x = x % (self.max_x)
        y = y % (self.max_y)

        self.p = (x, y)

    @classmethod
    def from_input(cls, line: str, max_x: int, max_y: int) -> "Robot":
        p, v = line.strip().split(" ")
        x, y = p.split("=")[1].split(",")
        vx, vy = v.split("=")[1].split(",")
        return cls((int(x), int(y)), (int(vx), int(vy)), max_x, max_y)


def calc(robots: list[Robot], max_x: int, max_y: int):
    q1 = 0
    q2 = 0
    q3 = 0
    q4 = 0

    mid_y = max_y // 2
    mid_x = max_x // 2

    for r in robots:
        x, y = r.p
        if x > mid_x and y > mid_y:
            q1 += 1
        elif x > mid_x and y < mid_y:
            q2 += 1
        elif x < mid_x and y > mid_y:
            q3 += 1
        elif x < mid_x and y < mid_y:
            q4 += 1

    return q1 * q2 * q3 * q4


def print_robots(robots: list[Robot], max_x: int, max_y: int):
    m = M.empty(max_x, max_y)
    for r in robots:
        x, y = r.p
        v = m.get(x, y)
        v = "1" if v == "." else str((int(v) + 1) % 10)
        m.set_item((x, y), v)
    m.print()


def logic(input: str, steps: int, max_x: int, max_y: int) -> int:
    lines = get_lines(input)
    robots = [Robot.from_input(line, max_x, max_y) for line in lines]
    for robot in robots:
        robot.move(steps)

    print_robots(robots, max_x, max_y)
    return calc(robots, max_x, max_y)


# --- Example ---


def test_example_1():
    example = """
    p=2,4 v=2,-3
    """
    lines = get_lines(example)
    robot = Robot.from_input(lines[0], 11, 7)
    robot.move(5)
    assert robot.p == (1, 3)


def test_example_2():
    example = """
    p=0,4 v=3,-3
    p=6,3 v=-1,-3
    p=10,3 v=-1,2
    p=2,0 v=2,-1
    p=0,0 v=1,3
    p=3,0 v=-2,-2
    p=7,6 v=-1,-3
    p=3,0 v=-1,-2
    p=9,3 v=2,3
    p=7,3 v=-1,2
    p=2,4 v=2,-3
    p=9,5 v=-3,-3
    """
    assert logic(example, 100, 11, 7) == 12


# --- Input ---


def test_input():
    result = logic(input, 100, 101, 103)
    assert result == 226236192
