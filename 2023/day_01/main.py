"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2
# forgot

import sys
sys.path.append(AOC_BASE_PATH := '/'.join(__file__.replace('\\', '/').split('/')[:-3]))
from aoc_tools import print_function, aoc_run
import re

AOC_ANSWER = (56397, 55701)
NUMBER_LUT = ('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine')

def clean_number_str(number: str) -> str:
    if number in NUMBER_LUT:
        return str(NUMBER_LUT.index(number) + 1)
    else:
        return number

def part_one(lines: list[str]) -> int:
    num_lines = [re.findall('\d', line) for line in lines]
    values = [int(nums[0] + nums[-1]) for nums in num_lines]
    return sum(values)

def part_two(lines: list[str]) -> int:
    num_lines = [re.findall('(?=(\d|' + '|'.join(NUMBER_LUT) + '))', line) for line in lines]
    values = [int(clean_number_str(nums[0]) + clean_number_str(nums[-1])) for nums in num_lines]
    return sum(values)
    
@print_function
def main(input: str) -> tuple[int, int]:
    lines = input.split('\n')
    return (part_one(lines), part_two(lines))

aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')
# aoc_run(__name__, __file__, main, AOC_ANSWER, 'ex')
