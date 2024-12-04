__all__ = ["get_lines"]


def get_lines(raw: str) -> list[str]:
    return [line.strip() for line in raw.strip().split("\n")]


def get_columns(lines: list[str]) -> list[str]:
    cols: list[str] = [""] * len(lines[0])

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            cols[x] = cols[x] + c if cols[x] else c

    return cols


def get_diagonals(lines: list[str]) -> tuple[list[str], list[str]]:
    size = len(lines)
    diag_1: list[str] = [""] * (2 * size - 1)
    diag_2: list[str] = [""] * (2 * size - 1)

    for x in range(size):
        for y in range(size):
            i = x + y
            i2 = size - 1 - x + y
            c = lines[y][x]
            diag_1[i] += c
            diag_2[i2] += c

    return diag_1, diag_2
