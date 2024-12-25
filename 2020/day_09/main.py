"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import itertools as it

AOC_ANSWER = (373803594, 51152360)

@print_function
def main(input_txt: str) -> tuple[int, int]:
    nums = list(map(int, input_txt.split('\n')))
    no_preamble = 25 if len(nums) == 1000 else 5
    for idx in range(no_preamble, len(nums)):
        for num1, num2 in it.combinations(nums[idx-no_preamble:idx], 2):
            if nums[idx] == num1 + num2:
                break
        else:
            break
    p1 = nums[idx]
    p2 = None
    for idx in range(len(nums)):
        ans = 0
        for idx2 in range(idx, len(nums)):
            ans += nums[idx2]
            if ans == p1:
                p2 = min(nums[idx:idx2+1]) + max(nums[idx:idx2+1])
            if ans >= p1:
                break
        if p2:
            break

    return p1, p2

aoc_run(__name__, __file__, main, AOC_ANSWER)
