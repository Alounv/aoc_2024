import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from day_11.test_11_1 import logic

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()


# --- Input ---


def test_part_2():
    result = logic(input, 75)
    assert result == 221280540398419
