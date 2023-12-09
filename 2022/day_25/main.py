"""
Advent of code challenge 2022
>> python3 main.py < in
Start   - 
Part 1  - 
Part 2  - 
Cleanup - 
"""

import sys
sys.path.insert(0, '/'.join(__file__.replace('\\', '/').split('/')[:-2]))
from _utils.print_function import print_function
import math

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
    

if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    lines = sys.stdin.read().strip().split('\n')

    solve_1(lines)