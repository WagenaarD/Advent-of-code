"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run

AOC_ANSWER = (1754, 1789)

@print_function
def main(input_txt: str) -> int:
    depths = list(map(int, input_txt.split('\n')))
    window_sums = [d1 + d2 + d3 for d1, d2, d3 in zip(depths, depths[1:], depths[2:])]
    return (
        sum(d2 > d1 for d1, d2 in zip(depths, depths[1:])),
        sum(d2 > d1 for d1, d2 in zip(window_sums, window_sums[1:])),
    )


aoc_run( __name__, __file__, main, AOC_ANSWER)
