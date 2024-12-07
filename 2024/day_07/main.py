"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

AOC_ANSWER = (8401132154762, 95297119227552)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import re
from operator import mul, add

def num_concat(a: int, b: int) -> int:
    """
    The concatenation operator (||) combines the digits from its left and right inputs into a single 
    number. For example, 12 || 345 would become 12345. All operators are still evaluated 
    left-to-right.
    """
    return int(str(a) + str(b))


def is_valid(result, nums, operators = [mul, add]):
    """
    Recursive function to evaluate whether equations could be true for a given set of mathematical
    operators. Operators are always evaluated left-to-right, not according to precedence rules. 
    """
    if len(nums) == 1:
        return nums[0] == result
    if nums[0] > result:
        return False
    for op in operators:
        new_nums = [op(nums[0], nums[1])] + nums[2:]
        if is_valid(result, new_nums, operators):
            return True
    return False


@print_function
def main(input: str) -> tuple[int, int]:
    p1, p2 = 0, 0
    for line in input.split('\n'):
        all_nums = list(map(int, re.findall('\\d+', line)))
        result, nums = all_nums[0], all_nums[1:]
        if is_valid(result, nums, [mul, add]):
            p1 += result
            p2 += result
        elif is_valid(result, nums, [mul, add, num_concat]):
            p2 += result
    return p1, p2


aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')


