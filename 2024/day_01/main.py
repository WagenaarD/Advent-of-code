"""
Advent of code challenge 2024
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (2285373, 21142653)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run


@print_function
def main(input: str) -> int:
    llist, rlist = [], []
    for line in input.split('\n'):
        lnum, rnum = map(int, line.split())
        llist.append(lnum)
        rlist.append(rnum)
    p1, p2 = 0, 0
    for nums in zip(sorted(llist), sorted(rlist)):
        p1 += max(nums) - min(nums)
        p2 += nums[0] * rlist.count(nums[0])
    return p1, p2

aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')
