import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities.parse import get_lines

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

# --- Logic ---


def to_int(b: bytes) -> int:
    return int.from_bytes(b, "big")


class Program:
    def __init__(self, input: str, instructions: list[int], A: int):
        self.input = input
        self.instr = instructions
        self.A = A
        self.has_A_changed = False
        self.indent = 0
        self.lines: list[tuple[int, str]] = []
        self.dispatch = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }
        self.build()
        self.code = "\n".join(map(lambda x: x[0] * "\t" + x[1], self.lines))
        print(self.code)

    def combo(self, v: int) -> str:
        match v:
            case 4:
                return "a"
            case 5:
                return "b"
            case 6:
                return "c"
            case 7:
                return "raise Exception"
            case _:
                return str(v)

    def adv(self, operand: int):
        self.has_A_changed = True
        self.add(f"a = a >> {self.combo(operand)}")

    def bxl(self, operand: int):
        self.add(f"b = b ^ {operand}")

    def bst(self, operand: int):
        self.add(f"b = {self.combo(operand)} & 7")

    def jnz(self, operand: int):
        if not self.has_A_changed:
            return
        start = self.offset + operand
        self.insert(start, "while a:")
        for i in range(start + 1, len(self.lines)):
            self.lines[i] = (self.indent + 1, self.lines[i][1])

        self.has_A_changed = False

    def bxc(self, operand: int):
        self.add("b = b ^ c")

    def out(self, operand: int):
        self.add(f"output.append({self.combo(operand)} & 7)")

    def bdv(self, operand: int):
        self.add(f"b = a >> {self.combo(operand)}")

    def cdv(self, operand: int):
        self.add(f"c = a >> {self.combo(operand)}")

    def add(self, s: str):
        self.lines.append((self.indent, s))

    def insert(self, index: int, s: str):
        self.lines.insert(index, (self.indent, s))

    def build(self):
        self.add("def my_func(a):")
        self.indent = 1

        self.add("b = 0")
        self.add("c = 0")
        self.add("output = []")
        self.add("")

        self.offset = len(self.lines)
        self.has_A_changed = False

        for i in range(0, len(self.instr) - 1, 2):
            op = self.instr[i]
            operand = self.instr[i + 1]
            self.dispatch[op](operand)

        self.add("")
        self.indent = 1
        self.add("return output")

    def run(self, A: int | None = None):
        exec(self.code, globals())
        result = globals()["my_func"](A or self.A)
        return ",".join(map(str, result))

    @classmethod
    def parse(cls, input: str) -> "Program":
        lines = get_lines(input)
        a = int(lines[0].split(":")[1])
        input = lines[4].split(":")[1].strip()
        numbers = list(map(int, input.split(",")))
        return cls(input, numbers, a)


def logic(input: str, i: int | None = None):
    program = Program.parse(input)
    return program.run(i)


# --- Example ---


def test_example_2():
    example = """
    Register A: 729
    Register B: 0
    Register C: 0

    Program: 0,1,5,4,3,0
    """
    assert logic(example) == "4,6,3,5,6,3,5,2,1,0"


# --- Input ---


def test_input():
    result = logic(input)
    assert result == "6,5,7,4,5,7,3,1,0"
