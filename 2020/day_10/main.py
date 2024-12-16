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

AOC_ANSWER = (2059, 86812553324672)

@print_function
def part_one(input_txt: str) -> int:
    nums = list(map(int, input_txt.split('\n')))
    diffs = defaultdict(int)
    jolt = 0
    while True:
        for inc in range(1, 4):
            njolt = jolt + inc
            if njolt in nums:
                diffs[inc] += 1
                jolt = njolt
                break
        else:
            break
    return diffs[1] * (diffs[3]+1)
    

@print_function
def part_two(input_txt: str) -> int:
    nums = list(map(int, input_txt.split('\n')))
    nums.sort()
    scores = defaultdict(int)
    scores[0] = 1
    for num in nums:
        for inc in range(1, 4):
            prev = num-inc
            scores[num] += scores[prev]
    return max(scores.values())


@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        part_one(input_txt), 
        part_two(input_txt)
    )
aoc_run(__name__, __file__, main, AOC_ANSWER)


