"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
from collections import defaultdict

AOC_ANSWER = (981, 164878)

def solve(input_txt: str, target_number: int) -> int:
    nums = list(map(int, input_txt.split(',')))
    last_spoken = defaultdict(int)
    for idx, num in enumerate(nums[:-1]):
        last_spoken[num] = idx
    num = nums[-1]
    for idx in range(idx+2, target_number):
        prev = num
        if prev not in last_spoken:
            num = 0
        else:
            num = idx - last_spoken[num] - 1
        last_spoken[prev] = idx - 1
    return num

@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        solve(input_txt, 2020), 
        solve(input_txt, 30_000_000)
    )
aoc_run(__name__, __file__, main, AOC_ANSWER)


