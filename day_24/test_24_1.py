import os
import sys
from enum import Enum
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities.parse import get_lines, get_parts

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()


class Op(Enum):
    AND = "AND"
    XOR = "XOR"
    OR = "OR"

    def run(self, a: bool, b: bool) -> bool:
        match self:
            case Op.AND:
                return a & b
            case Op.XOR:
                return a ^ b
            case Op.OR:
                return a | b

    def __str__(self):
        match self:
            case Op.AND:
                return "&"
            case Op.XOR:
                return "^"
            case Op.OR:
                return "|"

    def __repr__(self):
        return str(self)


Door = tuple[tuple[str, str], Op]


class Program:
    def __init__(
        self,
        bits: dict[str, bool],
        doors: dict[str, Door],
    ):
        self.initial_bits = bits
        self.bits = bits
        self.size = sum([1 for b in bits.keys() if b.startswith("x")])

        self.doors = doors
        self.doors_by_input = {}
        self.set_doors_by_default()

    def set_doors_by_default(self):
        for res, ((a, b), _) in self.doors.items():
            self.doors_by_input.setdefault(a, set()).add(res)
            self.doors_by_input.setdefault(b, set()).add(res)

    def get_bin(self, char, bits: dict[str, bool]):
        z_bits = [(b, v) for b, v in bits.items() if b.startswith(char)]
        z_bits = sorted(z_bits, key=lambda x: x[0], reverse=True)
        values = ["1" if v else "0" for _, v in z_bits]
        return "".join(values)

    def get_num(self, char, bits: dict[str, bool] | None = None):
        binary = self.get_bin(char, bits or self.bits)
        return int(binary, 2)

    def run(self):
        doors = list(self.doors.items())
        bits = self.bits.copy()

        while doors:
            has_loop = True
            for door in doors:
                res, ((a, b), op) = door
                if a not in bits or b not in bits:
                    continue

                has_loop = False
                a = bits[a]
                b = bits[b]
                bits[res] = op.run(a, b)

                doors.remove(door)
            if has_loop:
                return None

        return self.get_num("z", bits)

    def switch(self, ai: str, bi: str):
        p = self.copy()
        p.doors[ai], p.doors[bi] = p.doors[bi], p.doors[ai]
        return p

    def init(self):
        for b in self.bits:
            self.bits[b] = False

    def copy(self):
        return Program(self.bits, self.doors)

    def __str__(self):
        return f"{self.bits}\n{self.doors}"

    @classmethod
    def from_input(cls, input):
        p1, p2 = get_parts(input)

        p1 = get_lines(p1)
        p1 = [b.split(": ") for b in p1]
        bits = {name: v == "1" for name, v in p1}

        p2 = get_lines(p2)
        p2 = [d.split(" -> ") for d in p2]

        doors: dict[str, Door] = {}
        for op, res in p2:
            a, op, b = op.split(" ")
            doors.setdefault(res, ((a, b), Op(op)))

        return cls(bits, doors)


def logic(input: str):
    p = Program.from_input(input)
    return p.run()


# --- Example ---


def test_example_1():
    example = """
    x00: 1
    x01: 1
    x02: 1
    y00: 0
    y01: 1
    y02: 0

    x00 AND y00 -> z00
    x01 XOR y01 -> z01
    x02 OR y02 -> z02
    """
    assert logic(example) == 4


def test_example_2():
    example = """
    x00: 1
    x01: 0
    x02: 1
    x03: 1
    x04: 0
    y00: 1
    y01: 1
    y02: 1
    y03: 1
    y04: 1

    ntg XOR fgs -> mjb
    y02 OR x01 -> tnw
    kwq OR kpj -> z05
    x00 OR x03 -> fst
    tgd XOR rvg -> z01
    vdt OR tnw -> bfw
    bfw AND frj -> z10
    ffh OR nrd -> bqk
    y00 AND y03 -> djm
    y03 OR y00 -> psh
    bqk OR frj -> z08
    tnw OR fst -> frj
    gnj AND tgd -> z11
    bfw XOR mjb -> z00
    x03 OR x00 -> vdt
    gnj AND wpb -> z02
    x04 AND y00 -> kjc
    djm OR pbm -> qhw
    nrd AND vdt -> hwm
    kjc AND fst -> rvg
    y04 OR y02 -> fgs
    y01 AND x02 -> pbm
    ntg OR kjc -> kwq
    psh XOR fgs -> tgd
    qhw XOR tgd -> z09
    pbm OR djm -> kpj
    x03 XOR y03 -> ffh
    x00 XOR y04 -> ntg
    bfw OR bqk -> z06
    nrd XOR fgs -> wpb
    frj XOR qhw -> z04
    bqk OR frj -> z07
    y03 OR x01 -> nrd
    hwm AND bqk -> z03
    tgd XOR rvg -> z12
    tnw OR pbm -> gnj
    """
    assert logic(example) == 2024


# # --- Input ---


def test_input():
    result = logic(input)
    assert result == 45121475050728
