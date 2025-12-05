"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run

AOC_ANSWER = (712, 332998283036769)


@print_function
def part_one(input_txt: str) -> int:
    ranges_txt, ids_txt = input_txt.split('\n\n')
    ids = list(map(int, ids_txt.split('\n')))
    ranges = [list(map(int, range_txt.split('-'))) for range_txt in ranges_txt.split('\n')]
    score = 0
    for id in ids:
        for lower, upper in ranges:
            if lower <= id <= upper:
                score += 1
                break
    return score


@print_function
def part_two(input_txt: str) -> int:
    ranges_txt, _ = input_txt.split('\n\n')
    ranges = [list(map(int, range_txt.split('-'))) for range_txt in ranges_txt.split('\n')]
    # sort ranges so that the start of each range is increasing
    ranges.sort(key = lambda r: r[0])
    highest_upper = -1
    score = 0
    for lower, upper in ranges:
        # If upper bound is lower than the highest scored ingredient, this range has nothing to add
        if upper <= highest_upper:
            continue
        # We only start counting after the highest scored ingredient
        score += upper - max(lower, highest_upper + 1) + 1
        highest_upper = upper
    return score


@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        part_one(input_txt), 
        part_two(input_txt)
    )

aoc_run( __name__, __file__, main, AOC_ANSWER)
