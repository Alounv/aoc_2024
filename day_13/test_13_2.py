import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from day_13.test_13_1 import logic

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()


#  --- Input ---


offset = 10000000000000


def test_input():
    result = logic(input, offset)
    assert result == 108528956728655
