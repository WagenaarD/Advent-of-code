"""
From year folder:
../aoc_tools/aoc_start.sh xx && cd day_xx

Advent of code challenge
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (119433, 68466)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import json

def get_values(data: dict, ignore: str = '') -> int:
    if type(data) == int:
        return int(data)
    elif type(data) == list:
        return sum(get_values(val, ignore) for val in data)
    elif type(data) == dict:
        if ignore and ignore in data.values():
            return 0
        else:
            return sum(get_values(val, ignore) for val in data.values())
    else:
        assert type(data) in [str]
        return 0


@print_function
def main(input: str) -> tuple[int, int]:
    data = json.loads(input)
    return get_values(data), get_values(data, 'red')


aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')


