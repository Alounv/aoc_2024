import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from day_15.test_15_1 import Robot, get_next, parse_map, parse_moves, print_robot
from utilities.maps import M, P
from utilities.parse import get_parts

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logic ---


def scale_up(input: str) -> str:
    return (
        input.replace("#", "##")
        .replace("O", "[]")
        .replace(".", "..")
        .replace("@", "@.")
    )


def move_horizontal(map: M, first: P, move: str, robot: Robot):
    x, y = first
    prev = map.get(*first)
    dx = -1 if move == "<" else 1

    next_x = x + dx
    while True:
        curr = map.get(next_x, y)
        if curr == "#":
            return

        map.set_item((next_x, y), prev)
        if curr == ".":
            break

        prev = curr
        next_x += dx

    robot.p = first
    map.remove_item(first)


def get_next_boxes(map: M, x: int, y: int) -> set[int] | None:
    match map.get(x, y):
        case ".":
            return set()
        case "[":
            return {x, x + 1}
        case "]":
            return {x - 1, x}
        case "#":
            return None
        case _:
            raise Exception


def move_vertical(map: M, first: P, move: str, robot: Robot):
    x, first_y = first
    d = -1 if move == "^" else 1

    # Find boxes that can move
    boxes = []
    y = first_y
    prev_boxes = get_next_boxes(map, x, first_y)

    while prev_boxes:
        boxes.append((y, prev_boxes))
        y += d
        next_boxes = set()

        for x in prev_boxes:
            boxes_at_pos = get_next_boxes(map, x, y)
            if boxes_at_pos is None:
                return  # None means we ran into a wall
            next_boxes.update(boxes_at_pos)

        prev_boxes = next_boxes

    # Move robot and boxes
    robot.p = first
    for first_y, box_set in reversed(boxes):
        for x in box_set:
            map.switch((x, first_y), (x, first_y + d))


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
            if not is_pushing:
                robot.p = next
                break

            if is_pushing:
                if move in "<>":
                    move_horizontal(map, next, move, robot)
                else:
                    move_vertical(map, next, move, robot)
                break

        if char in "[]" and not is_pushing:
            # say we are pushing at least one O
            is_pushing = True

        p = get_next(p, move)

    # print_robot(robot, map, clean=True)


def calc(map: M) -> int:
    boxes = map.find_all("[")
    return sum(x + 100 * y for x, y in boxes)


def logic(input: str) -> int:
    map, moves = get_parts(input)
    moves = parse_moves(moves)
    map, robot = parse_map(scale_up(map))

    [move(robot, mv, map) for mv in moves]

    print_robot(robot, map, clean=True)
    return calc(map)


# --- Example ---


def test_scale_up():
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
    """
    assert (
        scale_up(example)
        == """
    ####################
    ##....[]....[]..[]##
    ##............[]..##
    ##..[][]....[]..[]##
    ##....[]@.....[]..##
    ##[]##....[]......##
    ##[]....[]....[]..##
    ##..[][]..[]..[][]##
    ##........[]......##
    ####################
    """
    )


def test_example_1():
    example = """
    #######
    #...#.#
    #.....#
    #..OO@#
    #..O..#
    #.....#
    #######

    <vv<<^^<<^^
    """
    assert logic(example) == 105 + 207 + 306


def test_example_3():
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
    assert logic(example) == 9021


# # --- Input ---


def test_input():
    result = logic(input)
    assert result == 1429013
