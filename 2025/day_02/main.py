"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import re

AOC_ANSWER = (31839939622, 41662374059)


@print_function
def main(input_txt: str) -> int:
    score_p1, score_p2 = 0, 0
    for range_txt in input_txt.split(','):
        lower, upper = map(int, range_txt.split('-'))
        for idx in range(lower, upper+1):
            # Regex explainer
            # (\\d+) matches digits of any length and stores it as a group (group 1)
            # (\\1) is the same as the first group (group 1)
            # + allows for 1 or more repititions of the same kind
            match = re.fullmatch('(\\d+)(\\1)+', str(idx))
            if match:
                score_p2 += idx
                # If there were two matches, group 1 should be half the length of the total string
                if len(match.groups()[0]) == len(str(idx)) / 2:
                    score_p1 += idx
    return score_p1, score_p2



aoc_run( __name__, __file__, main, AOC_ANSWER)
