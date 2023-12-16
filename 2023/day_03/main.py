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
sys.path.append('../..')
from aoc_tools import print_function
import re
import math
from time import time
from collections import namedtuple

AOC_ANSWER = (557705, 84266818)
ADJACENT = tuple((r, c) for r in range(-1, 2) for c in range(-1, 2) if (r, c) != (0,0))
NON_SYMBOLS = '1234567890.'

@print_function()
def main(input: str) -> tuple[int, int]:
    lines = input.split('\n')
    nrows, ncols = len(lines), len(lines[0])
    score_p1 = 0
    score_p2 = 0
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char in NON_SYMBOLS:
                continue
            # Find coordinates of the start of adjacent numbers
            num_coords = set()
            for rr, cc in ADJACENT:
                if not (0 <= r + rr < nrows and 0 <=  c + cc < ncols):
                    continue
                if not lines[r + rr][c + cc].isdigit():
                    continue
                while (c + cc) > 0 and lines[r + rr][c + cc - 1].isdigit():
                    cc -= 1
                num_coords.add((r + rr, c + cc))
            
            # Find nums
            nums = [int(re.match('\d+', lines[nr][nc:]).group()) for nr, nc in num_coords]
            score_p1 += sum(nums)
            if char == '*' and len(nums) == 2:
                score_p2 += math.prod(nums)
    return (score_p1, score_p2)


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    input = sys.stdin.read().strip()
    print('  ->', main(input) == (AOC_ANSWER[0], AOC_ANSWER[1]))