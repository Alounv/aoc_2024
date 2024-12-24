import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from day_23.test_23_1 import Graph, find_for_size

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()


def find(g: Graph, max: int) -> set[tuple[str]]:
    solutions = set()

    for i, name in enumerate(g.names):
        node = (name, g.nodes[name])
        for_size = find_for_size(g, node, g.names[:i], max)
        solutions.update(for_size)

    return solutions


def logic(input: str):
    g = Graph.from_input(input)

    for i in range(1, len(g.names) + 1):
        solutions = find(g, i)

        if len(solutions) > 1:
            continue

        if len(solutions) < 1:
            raise ValueError("No solutions found")

        return solutions.pop()

    return None


# --- Example ---


def test_example_1():
    example = """
    kh-tc
    qp-kh
    de-cg
    ka-co
    yn-aq
    qp-ub
    cg-tb
    vc-aq
    tb-ka
    wh-tc
    yn-cg
    kh-ub
    ta-co
    de-co
    tc-td
    tb-wq
    wh-td
    ta-ka
    td-qp
    aq-cg
    wq-ub
    ub-vc
    de-ta
    wq-aq
    wq-vc
    wh-yn
    ka-de
    kh-ta
    co-tc
    wh-qp
    tb-vc
    td-yn
    """
    assert logic(example) == "co,de,ka,ta"


# --- Input ---


def test_input():
    result = logic(input)
    assert result == "az,cg,ei,hz,jc,km,kt,mv,sv,sx,wc,wq,xy"
