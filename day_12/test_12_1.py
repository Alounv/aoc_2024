import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities.maps import M, P, get_neighbors

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logic ---


class Area:
    def __init__(self, first: P, type: str):
        self.points = {first}
        self.type = type

    def dim(self) -> tuple[int, int]:
        xs = [x for x, _ in self.points]
        ys = [y for _, y in self.points]
        return max(xs) + 1, max(ys) + 1

    def has(self, point: P) -> bool:
        return point in self.points

    def count_adjacent(self, point: P) -> int:
        return sum(neighbor in self.points for neighbor in get_neighbors(point))

    def has_border(self, point: P, side: str) -> bool:
        x, y = point
        match side:
            case "left":
                return (x - 1, y) not in self.points
            case "right":
                return (x + 1, y) not in self.points
            case "top":
                return (x, y - 1) not in self.points
            case "bottom":
                return (x, y + 1) not in self.points
        raise ValueError(f"Invalid side: {side}")

    def add(self, point: P) -> bool:
        adjacent = self.count_adjacent(point)
        if adjacent == 0:
            return False

        self.points.add(point)
        return True

    def touch(self, other: "Area") -> bool:
        for p in self.points:
            for n in get_neighbors(p):
                if n in other.points:
                    return True
        return False

    def merge(self, other: "Area"):
        other_border = other.points

        while len(other_border) > 0:
            points = other_border.copy()
            for p in points:
                if self.add(p):
                    other_border.remove(p)

    def print(self, width: int, height: int):
        str = "\n".join("." * width for _ in range(height))
        map = M(str)
        map = map.merge(self.points, self.type)
        map.print()


def merge_areas(areas: list[Area]) -> bool:
    has_merged = False
    for area in areas:
        for other in areas:
            if area is other:
                continue
            if area.touch(other):
                has_merged = True
                area.merge(other)
                areas.remove(other)

    return has_merged


def get_area(points: list[P], type: str) -> list[Area]:
    areas = []

    # naive area creation
    for p in points:
        is_new_area = True

        for area in areas:
            if area.add(p):
                is_new_area = False
                break

        if is_new_area:
            areas.append(Area(p, type))

    # merge areas until no more merges
    has_merged = True
    while has_merged:
        has_merged = merge_areas(areas)

    return areas


def get_areas(map: M) -> list[Area]:
    areas = []
    types = map.list_points()

    areas = []
    for type, points in types.items():
        type_areas = get_area(points, type)
        areas.extend(type_areas)

    return areas


def calc_perimeter(area: Area) -> int:
    sum = 0
    for p in area.points:
        sum += 4 - area.count_adjacent(p)
    return sum


def logic(input: str) -> int:
    map = M(input)
    areas = get_areas(map)
    return sum(calc_perimeter(area) * len(area.points) for area in areas)


# --- Example ---


def test_example_1():
    example = """
    AAAA
    BBCD
    BBCC
    EEEC
    """
    assert logic(example) == 140


def test_example_2():
    example = """
    OOOOO
    OXOXO
    OOOOO
    OXOXO
    OOOOO
    """
    assert logic(example) == 772


def test_example_3():
    example = """
    ..II......
    ..II......
    ...........
    ...........
    ...........
    ..I.......
    ..III.....
    .IIIII....
    .III.I....
    ...........
    """
    assert logic(example) == 292


def test_example_4():
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
    assert logic(example) == 1930


# --- Input ---


def test_input():
    result = logic(input)
    assert result == 1486324
