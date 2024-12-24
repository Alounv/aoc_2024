import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from day_21.test_21_1 import logic

input_path = Path(__file__).parent / "input.txt"
input = input_path.read_text()


# --- Input ---


def test_input():
    result = logic(input, 25)
    assert result == 189235298434780
