import os
import sys
from pathlib import Path
from typing import Callable

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from day_24.test_24_1 import Door, Op, Program

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()


def get_doors(p: Program, i: int) -> frozenset[str]:
    zi = f"z{i:02d}"
    z = p.doors[zi]
    return frozenset({zi, z[0][0], z[0][1]})


def find_and_sort(p: Program, f: Door, s: Door, first_expected: Door):
    operands = {*first_expected[0]}
    op = first_expected[1]
    a = None
    for x in (f, s):
        if operands == {*x[0]} and x[1] == op:
            a = x
    b = s if a is f else f
    return a, b


# for addition
#
# Z = A XOR B
# A = X XOR Y
# B = C AND D
# C = PREV_X AND PREV_Y
# D = PREV_A AND PREV_B


def check_door(p: Program, i: int):
    if i <= 2:
        return True

    # Z calculation
    z = p.doors[f"z{i:02d}"]
    fi, si = z[0]
    f, s = p.doors.get(fi, None), p.doors.get(si, None)
    if f is None or s is None:
        return False

    # A and B calculation (look for A as X XOR Y, B is the other one)
    a, b = find_and_sort(p, f, s, ((f"x{i:02d}", f"y{i:02d}"), Op.XOR))
    if a is None or b is None:
        return False

    fb, sb = p.doors.get(b[0][0], None), p.doors.get(b[0][1], None)
    if fb is None or sb is None:
        return False

    # C and D calculation (look for C as PREV_X AND PREV_Y, D is the other one)
    c, d = find_and_sort(p, fb, sb, ((f"x{i-1:02d}", f"y{i-1:02d}"), Op.AND))

    # Check D operands are PREV_A AND PREV_B and op is AND
    prev_z = p.doors.get(f"z{i-1:02d}", None)
    assert prev_z
    if d[1] != Op.AND or {*d[0]} != {*prev_z[0]}:
        return False

    return True


def logic(input: str, op: Callable = lambda x, y: x + y):
    def recurse(
        p: Program, i: int, non_checked: set[str], solutions: list[set[str]]
    ) -> list[set[str]] | None:
        if i == p.size:
            return solutions

        if check_door(p, i):
            s = recurse(p, i + 1, non_checked, solutions)
            if s is not None:
                return s

        doors = get_doors(p, i)
        doors_to_test = frozenset(doors.intersection(non_checked))

        pairs = [(a, b) for a in doors_to_test for b in (non_checked) if a != b]
        for a, b in pairs:
            p.switch(a, b)

            if check_door(p, i):
                s = recurse(p, i + 1, non_checked, solutions + [{a, b}])
                if s is not None:
                    return s

            p.switch(a, b)

    p = Program.from_input(input)
    p.init()
    non_checked = set(p.doors.keys())
    solutions = recurse(p, 0, non_checked, [])
    assert solutions is not None

    final = set()
    for s in solutions:
        final.update(s)
    return ",".join(sorted(final))


# --- Input ---


def test_input():
    result = logic(input)
    assert result == "gqp,hsw,jmh,mwk,qgd,z10,z18,z33"
