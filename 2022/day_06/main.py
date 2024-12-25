"""
Advent of code challenge 2022
Start  17:37
Part 1 17:39 - 1480
Part 2 17:44 - 2746
Clean  17:48 
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run

AOC_ANSWER = (1480, 2746)


def find_distinct_substring(input_txt: str, length: int) -> int:
    for idx in range(len(input_txt)):
        if len(set(input_txt[idx:idx+length])) == length:
            return idx + length 

@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        find_distinct_substring(input_txt, 4), 
        find_distinct_substring(input_txt, 14),
    )

aoc_run(__name__, __file__, main, AOC_ANSWER)