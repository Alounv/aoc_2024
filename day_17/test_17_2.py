import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from day_17.test_17_1 import Program, logic

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logc ---


# output from part 1
def my_func(a):
    b = 0
    c = 0
    output = []

    while a:
        b = a & 7
        b = b ^ 5
        c = a >> b
        a = a >> 3
        b = b ^ 6
        b = b ^ c
        output.append(b & 7)

    return output


# we can simplify the logic this way (a only depends on the digit index)
def get_digit(A: int, index: int):
    a = A >> (3 * index)
    result = (((a & 7) ^ 5 ^ 6) ^ (a >> ((a & 7) ^ 5))) & 7
    return result, a == 0


# check we can reproduce logic from part 1 with the new get_digit
def my_func_2(a: int):
    d = []

    for i in range(10):
        r, is_null = get_digit(a, i)
        if is_null:
            break
        d.append(r)

    return d


# helper to check if a solution is correct
def check(a: int, input: list[int]):
    for i in range(len(input)):
        if get_digit(a, i)[0] != input[i]:
            return False
    return True


# recursive check the solution for each digit
def find(value: int, input: list[int], index: int) -> set[int]:
    if len(input) == index:
        return {value}

    solutions = set()

    for j in range(0, 8):
        # this is how we add the new octal digit to existing octal number
        next = (value << 3) + j
        input_so_far = input[-index - 1 :]

        if check(next, input_so_far):
            r = find(next, input, index + 1)
            solutions.update(r)

    return solutions


def logic_2(input: str) -> int:
    p = Program.parse(input)
    solutions = find(0, p.instr, 0)
    return min(solutions)


# --- Example ---


def test_example_1():
    example = """
    Register A: 2024
    Register B: 0
    Register C: 0

    Program: 0,3,5,4,3,0
    """

    assert logic(example, 117440)


# --- Input ---


def test_my_func():
    A = Program.parse(input).A

    # check my_func is correct
    r1 = my_func(A)
    assert ",".join(map(str, r1)) == "6,5,7,4,5,7,3,1,0"

    # check get_digit works fine
    r2 = my_func_2(A)
    assert r1 == r2


def test_input():
    instr = Program.parse(input).instr
    result = logic_2(input)
    assert check(result, instr)
    assert result == 105875099912602
