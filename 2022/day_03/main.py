"""
Advent of code challenge 2022
"""

__project__   = 'Advent of code 2022'
__author__    = 'D W'

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import string

AOC_ANSWER = (7795, 2703)


def get_char_priority(char: str) -> int:
    """
    Every item type can be converted to a priority:
     - Lowercase item types a through z have priorities 1 through 26.
     - Uppercase item types A through Z have priorities 27 through 52.
    """
    return string.ascii_letters.find(char) + 1 


def line_score(backpack: str) -> int:
    """
    Backpack is a string of even lenght of which the first and second halves are considered in 
    different compartments.
    Finds the char that is present in both compartments and returns its priority
    """
    comp_1 = backpack[0:len(backpack) // 2]
    comp_2 = backpack[len(backpack) // 2:]
    for char in comp_1:
        if char in comp_2:
            return get_char_priority(char)
    else:
        raise(Exception('WTF: no char found in both compartments for line: "{}"'.format(backpack)))


def badge_score(backpack_list: list) -> int:
    """
    Finds the char that is present in all three backpacks and returns its priority
    """
    for char in backpack_list[0]:
        if all([char in backpack for backpack in backpack_list[1:]]):
            return get_char_priority(char)
    else:
         raise(Exception('WTF: no badge found in group: "{}"'.format(backpack_list)))


@print_function
def main(input_txt: str) -> tuple[int, int]:
    lines = input_txt.split('\n')
    sum_lines = sum([line_score(line) for line in lines])
    sum_badges = sum([badge_score(lines[idx:idx + 3]) for idx in range(0, len(lines), 3)])
    return sum_lines, sum_badges

aoc_run(__name__, __file__, main, AOC_ANSWER)
