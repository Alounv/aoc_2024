import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities.maps import M, P
from utilities.parse import get_parts

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logic ---


MOVES = {">": (1, 0), "<": (-1, 0), "^": (0, -1), "v": (0, 1)}


def get_next(p: P, move: str) -> P:
    x, y = p
    dx, dy = MOVES[move]
    return x + dx, y + dy


class Robot:
    def __init__(self, p: P):
        self.p = p

    def __str__(self):
        return f"P: {self.p}"


def parse_map(input: str):
    map = M(input)
    robot = map.find_one("@")
    assert robot
    map.remove_item(robot)
    return map, Robot(robot)


def parse_moves(input: str):
    return input.replace("\n", "").replace(" ", "")


def print_robot(robot: Robot, map: M, clean: bool = False):
    (map.merge({robot.p}, "@")).print({"@": 13, "#": 10, "[": 4, "]": 3}, clean)


def move(robot: Robot, move: str, map: M):
    is_pushing = False
    next = get_next(robot.p, move)
    p = next

    while True:
        char = map.get(*p)

        if char == "#":
            # cannot move
            break

        if char == ".":
            # can move
            robot.p = next
            if is_pushing:
                # Os ares pushed
                map.remove_item(next)
                map.set_item(p, "O")
            break

        if char == "O" and not is_pushing:
            # say we are pushing at least one O
            is_pushing = True

        p = get_next(p, move)


def calc(map: M) -> int:
    boxes = map.find_all("O")
    return sum(x + 100 * y for x, y in boxes)


def logic(input: str) -> int:
    map, moves = get_parts(input)
    moves = parse_moves(moves)
    map, robot = parse_map(map)

    [move(robot, mv, map) for mv in moves]
    return calc(map)


# --- Example ---


def test_example_1():
    example = """
    ########
    #..O.O.#
    ##@.O..#
    #...O..#
    #.#.O..#
    #...O..#
    #......#
    ########

    <^^>>>vv<v>>v<<
    """
    assert logic(example) == 2028


def test_example_2():
    example = """
    ##########
    #..O..O.O#
    #......O.#
    #.OO..O.O#
    #..O@..O.#
    #O#..O...#
    #O..O..O.#
    #.OO.O.OO#
    #....O...#
    ##########

    <vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
    vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
    ><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
    <<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
    ^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
    ^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
    >^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
    <><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
    ^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
    v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
    """
    assert logic(example) == 10092


# --- Input ---


def test_input():
    result = logic(input)
    assert result == 1406392
