"""
Advent of code challenge
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (270144, 261342720)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run


@print_function
def part_one(input: str) -> int:
    nums = list(map(int, input.split('\n')))
    for idx, num in enumerate(nums):
        for other in nums[idx+1:]:
            if num + other == 2020:
                return num * other

@print_function
def part_two(input: str) -> int:
    nums = list(map(int, input.split('\n')))
    for idx_1, num_1 in enumerate(nums):
        for idx_2, num_2 in enumerate(nums[idx_1+1:]):
            for num_3 in nums[idx_1+idx_2+1:]:
                if num_1 + num_2 + num_3 == 2020:
                    return num_1 * num_2 * num_3


@print_function
def main(input: str) -> tuple[int, int]:
    return (
        part_one(input), 
        part_two(input)
    )
aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')


