"""
Advent of code challenge 2022
>> python3 main.py < in
Start   - 
Part 1  - 
Part 2  - 
Cleanup - 
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import math

AOC_ANSWER = ('2-=2==00-0==2=022=10', None)
SNAFU_DIGIT_LUT = {'2': 2, '1': 1, '0': 0, '-': -1, '=':  -2}
DIGIT_SNAFU_LUT = {val: key for key, val in SNAFU_DIGIT_LUT.items()}


def snafu_to_dec(line: str) -> int:
    val = 0
    dig = 1
    for char in line[::-1]:
        val += dig * SNAFU_DIGIT_LUT[char]
        dig *= 5
    return val 


def dec_to_snafu(val: int) -> str:
    # Convert to list of base 5 nunbers
    digits = [0] * (int(math.log(val, 5)) + 1)
    remainder = val
    while remainder:
        max_base = int(math.log(remainder, 5))
        digits[max_base] += 1
        remainder -= 5 ** max_base
    
    # Carry over out-of-bounds digits
    for idx in range(len(digits)):
        while digits[idx] > 2:
            if idx == len(digits) - 1:
                digits.append(0)
            digits[idx] -= 5
            digits[idx + 1] += 1

    # Remove trailing 0s
    while digits[-1] == 0:
        digits.pop()

    return ''.join([DIGIT_SNAFU_LUT[dig] for dig in digits[::-1]])

    
@print_function()
def solve_1(lines):
    total_value_dec = sum(snafu_to_dec(line) for line in lines)
    return dec_to_snafu(total_value_dec)
    

@print_function
def main(input_txt: str) -> tuple[int, int]:
    lines = input_txt.split('\n')

    return (solve_1(lines), None)

aoc_run(__name__, __file__, main, AOC_ANSWER)
