import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities.maps import P
from utilities.parse import get_parts

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logic ---


def parse_prize(line: str, offset: int) -> P:
    _, x, y = line.split(" ")
    x = x.split("=")[1].strip(",")
    y = y.split("=")[1]
    return int(x) + offset, int(y) + offset


def parse_button(line: str) -> P:
    _, _, x, y = line.split(" ")
    x = x.split("+")[1].strip(",")
    y = y.split("+")[1]
    return (int(x), int(y))


class Machine:
    def __init__(self, a: P, b: P, prize: P):
        self.a = a
        self.b = b
        self.prize = prize

    def __str__(self):
        return f"A: {self.a}\nB: {self.b}\nP: {self.prize[0]}, {self.prize[1]}"

    @classmethod
    def from_input(cls, input: str, offset: int = 0) -> "Machine":
        lines = [line.strip() for line in input.strip().split("\n")]
        a = parse_button(lines[0])
        b = parse_button(lines[1])
        prize = parse_prize(lines[2], offset)
        return cls(a, b, prize)


def solve(X, Y, a_x, a_y, b_x, b_y):
    # X = a * a_x + b * b_x
    # Y = a * a_y + b * b_y

    det = a_x * b_y - b_x * a_y

    if det == 0:
        return None

    a_float = (X * b_y - b_x * Y) / det
    b_float = (a_x * Y - X * a_y) / det

    a = int(a_float)
    b = int(b_float)

    if a != a_float or b != b_float:
        return None

    return (a, b)


def calc(m: Machine):
    r = solve(*m.prize, *m.a, *m.b)
    a, b = (0, 0) if r is None else r
    return a * 3 + b


def logic(input: str, offset: int = 0) -> int:
    parts = get_parts(input)

    sum = 0
    for part in parts:
        m = Machine.from_input(part, offset)
        sum += calc(m)

    return sum


# --- Example ---


def test_example_1():
    example = """
    Button A: X+94, Y+34
    Button B: X+22, Y+67
    Prize: X=8400, Y=5400
    """

    assert logic(example) == 280


def test_example_2():
    example = """
    Button A: X+26, Y+66
    Button B: X+67, Y+21
    Prize: X=12748, Y=12176
    """
    assert logic(example) == 0


def test_example_3():
    example = """
    Button A: X+17, Y+86
    Button B: X+84, Y+37
    Prize: X=7870, Y=6450
    """
    assert logic(example) == 200


def test_example_4():
    example = """
    Button A: X+69, Y+23
    Button B: X+27, Y+71
    Prize: X=18641, Y=10279
    """
    assert logic(example) == 0


def test_example_5():
    example = """
    Button A: X+94, Y+34
    Button B: X+22, Y+67
    Prize: X=8400, Y=5400

    Button A: X+26, Y+66
    Button B: X+67, Y+21
    Prize: X=12748, Y=12176

    Button A: X+17, Y+86
    Button B: X+84, Y+37
    Prize: X=7870, Y=6450

    Button A: X+69, Y+23
    Button B: X+27, Y+71
    Prize: X=18641, Y=10279
    """
    assert logic(example) == 480


# --- Input ---


def test_input():
    result = logic(input)
    assert result == 25751
