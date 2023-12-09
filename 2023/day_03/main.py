"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2
# 09:26:18
# 09:38:09  11:51
# 09:47:59  21:41

import sys
sys.path.append('..')
from aoc_tools import print_function
import re
import math

AOC_ANSWER = (557705, 84266818)
            
@print_function()
def main(input: 'str'):
    # Make lists of all digits, gears and symbols. Digits include a list of all bounding box coords
    digits = []
    gears = []
    symbols = []
    for r, line in enumerate(input.split('\n')):
        for c, char in enumerate(line):
            if char == '*':
                gears.append((r, c))
            if char not in '1234567890.':
                symbols.append((r, c))
        for re_match in re.finditer('\d+', line):
            value_str = re_match.group()
            c = re_match.start()
            value = int(value_str)
            digits.append((value, [(r + rr, c + cc) for rr in (-1,0,1) for cc in range(-1,1+len(value_str))]))
    # Scoring
    score_p1 = 0
    for dig in digits:
        adjacent = [sym for sym in symbols if sym in dig[1]]
        if adjacent:
            score_p1 += dig[0]
    score_p2 = 0
    for gear in gears:
        adjacent_digits = [dig[0] for dig in digits if gear in dig[1]]
        if len(adjacent_digits) == 2:
            score_p2 += math.prod(adjacent_digits)

    return (score_p1, score_p2)


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    input = sys.stdin.read().strip()
    print('  ->', main(input) == (AOC_ANSWER[0], AOC_ANSWER[1]))