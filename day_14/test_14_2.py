import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from day_14.test_14_1 import Robot, print_robots
from utilities.parse import get_lines

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logic ---


def logic(input: str, steps: int, max_x: int, max_y: int) -> int:
    lines = get_lines(input)
    robots = [Robot.from_input(line, max_x, max_y) for line in lines]
    for robot in robots:
        robot.move(steps)

    print("\n")
    print(steps)
    print_robots(robots, max_x, max_y)
    return 0


def solve():
    # A = 88 + 101x = 134 + 103y
    # x = (103y + 46)/101
    y = 0
    while True:
        d = 103 * y + 46
        if d % 101 == 0:
            print("----", y)
            break
        y += 1
    return 134 + 103 * y


# --- Input ---


def test_input_vertical():
    logic(input, 88, 101, 103)
    logic(input, 88 + 101, 101, 103)
    logic(input, 88 + 2 * 101, 101, 103)
    assert 0 == 0


def test_input_horizontal():
    logic(input, 134, 101, 103)
    logic(input, 134 + 103, 101, 103)
    logic(input, 134 + 2 * 103, 101, 103)
    assert 0 == 0


def test_input():
    result = solve()
    logic(input, result, 101, 103)

    assert result == 8168
