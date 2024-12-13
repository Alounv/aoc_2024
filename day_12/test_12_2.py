import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from day_12.test_12_1 import Area, get_areas
from utilities.maps import M, P

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logic ---


def get_side_borders(area: Area) -> tuple[set[P], set[P], set[P], set[P]]:
    result = (set(), set(), set(), set())
    for p in area.points:
        if area.has_border(p, "top"):
            result[0].add(p)
        if area.has_border(p, "right"):
            result[1].add(p)
        if area.has_border(p, "bottom"):
            result[2].add(p)
        if area.has_border(p, "left"):
            result[3].add(p)
    return result


def filter_y(points: set[P], y: int) -> list[P]:
    return list(filter(lambda p: p[1] == y, points))


def filter_x(points: set[P], x: int) -> list[P]:
    return list(filter(lambda p: p[0] == x, points))


def get_x(points: list[P]):
    return set([x for x, _ in points])


def get_y(points: list[P]):
    return set([y for _, y in points])


def calc_x(points: set[P], prev: set[int], y: int) -> tuple[int, set[int]]:
    sides = 0
    step_points = filter_y(points, y)
    for x, y in step_points:
        sides += 1 if x not in prev else 0
    return sides, get_x(step_points)


def calc_y(points: set[P], prev: set[int], x: int) -> tuple[int, set[int]]:
    sides = 0
    step_points = filter_x(points, x)
    for x, y in step_points:
        sides += 1 if y not in prev else 0
    return sides, get_y(step_points)


def calc_sides(area: Area) -> int:
    top, right, bottom, left = get_side_borders(area)
    max_x, max_y = area.dim()

    t_prev_y, r_prev_x, b_prev_y, l_prev_x = set(), set(), set(), set()
    sides = 0

    for y in range(max_y):
        l_sides, l_prev_x = calc_x(left, l_prev_x, y)
        r_sides, r_prev_x = calc_x(right, r_prev_x, y)
        sides += l_sides + r_sides

    for x in range(max_x):
        t_sides, t_prev_y = calc_y(top, t_prev_y, x)
        b_sides, b_prev_y = calc_y(bottom, b_prev_y, x)
        sides += t_sides + b_sides

    return sides


def logic(input: str) -> int:
    map = M(input)
    areas = get_areas(map)
    return sum(calc_sides(area) * len(area.points) for area in areas)


# --- Example ---


def test_example_1():
    example = """
    AAAA
    BBCD
    BBCC
    EEEC
    """
    assert logic(example) == 80


def test_example_2():
    example = """
    OOOOO
    OXOXO
    OOOOO
    OXOXO
    OOOOO
    """
    assert logic(example) == 436


def test_example_3():
    example = """
    EEEEE
    EXXXX
    EEEEE
    EXXXX
    EEEEE
    """

    areas = get_areas(M(example))
    test = calc_sides(areas[0])
    print(test)
    assert logic(example) == 236


def test_example_4():
    example = """
    AAAAAA
    AAABBA
    AAABBA
    ABBAAA
    ABBAAA
    AAAAAA
    """
    assert logic(example) == 368


def test_example_5():
    example = """
    RRRRIICCFF
    RRRRIICCCF
    VVRRRCCFFF
    VVRCCCJFFF
    VVVVCJJCFE
    VVIVCCJJEE
    VVIIICJJEE
    MIIIIIJJEE
    MIIISIJEEE
    MMMISSJEEE
    """
    assert logic(example) == 1206


# # --- Input ---


def test_input():
    result = logic(input)
    assert result == 898684
