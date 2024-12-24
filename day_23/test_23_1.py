import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities.parse import get_lines

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()

Node = tuple[str, set[str]]


class Graph:
    def __init__(self, links: list[tuple[str, str]]):
        self.nodes: dict[str, set[str]] = {}
        self.links: list[tuple[str, str]] = []
        for a, b in links:
            self.nodes.setdefault(a, set()).add(b)
            self.nodes.setdefault(b, set()).add(a)
            self.links.append((a, b))
            self.links.append((b, a))

        self.names = sorted(list(self.nodes))
        self.size = len(self.nodes)

    def all_linked(self, points: list[str]) -> bool:
        for a in points:
            for b in points:
                if a == b:
                    continue
                if (a, b) not in self.links:
                    return False
        return True

    @classmethod
    def from_input(cls, input: str):
        links = []
        for line in get_lines(input):
            a, b = line.split("-")
            links.append((a, b))
        return cls(links)

    def __str__(self):
        return "\n".join(f"{a} -> {b}" for a, b in self.nodes.items())


def find_for_size(g: Graph, node: Node, rest: list[str], size: int) -> set[str]:
    solutions = set()

    # recursion
    def recurse(net, rest, steps, net_links):
        if steps == size:
            key = ",".join(sorted(net))
            solutions.add(key)
            return

        for i, name in enumerate(rest):
            if name not in net_links:
                continue

            links = g.nodes[name]

            recurse(
                net + [name],
                rest[:i],
                steps + 1,
                links.intersection(net_links),
            )

    # initial call
    recurse(
        [node[0]],
        rest,
        1,
        node[1],
    )

    return solutions


def find(g: Graph, max: int) -> set[str]:
    solutions = set()

    t_names = [n for n in g.names if n[0] == "t"]
    for n in t_names:
        node = (n, g.nodes[n])
        for_size = find_for_size(g, node, g.names, max)
        solutions.update(for_size)

    return solutions


def logic(input: str):
    g = Graph.from_input(input)
    solutions = find(g, 3)
    return len(solutions)


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
    assert logic(example) == 7


# --- Input ---


def test_input():
    result = logic(input)
    assert result == 1075
