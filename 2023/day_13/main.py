"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (None, None)

import sys
sys.path.append('../..')
from aoc_tools import *
import itertools as it
from dataclasses import dataclass, field
from collections import defaultdict
import re
import numpy as np
from pprint import pprint
from functools import cache
import math

# To summarize your pattern notes, add up the number of columns to the left of each vertical line of 
# reflection; to that, also add 100 multiplied by the number of rows above each horizontal line of 
# reflection. In the above example, the first pattern's vertical line has 5 columns to its left and 
# the second pattern's horizontal line has 4 rows above it, a total of 405.


@print_function()
def f(b):    
    
    for idx in range(1, len(b)):
        up = list(reversed(b[:idx]))
        down = b[idx:]
        sz = min(len(up), len(down))
        valid = ''.join(up[:sz]) == ''.join(down[:sz])
        
        # print('')
        # print(idx, valid)
        # print('\n'.join(up))
        # print('============')
        # print('\n'.join(down))
        # if idx == 3:
        #     print(''.join(up[:sz]))
        #     print(''.join(down[:sz]))
        #     print(valid)
        #     exit()

        
        if valid:
            print('\nSymmetry found')
            for line_idx, line in enumerate(b, 1):
                if line_idx == idx:
                    print('-' * (len(line)+6))
                    print(f'{line_idx:3} {line}')
                else:
                    print(f'{line_idx:3} {line}')
            return idx
    return 0


def transpose_block(b: str) -> str:
    """Transposes B"""
    b = [list(r) for r in b]
    bt = [[''] * len(b) for idx in range(len(b[0]))]
    # print('b', len(b), len(b[0]))
    # print('bt', len(bt), len(bt[0]))
    
    for r, row in enumerate(b):
        for c, char in enumerate(row):
            bt[c][r] = char
    return [''.join(row) for row in bt]

@print_function()
def main(input: str) -> int:
    bs = input.split('\n\n')
    
    ans = 0
    for b in bs:
        b = b.split('\n')
        bt = transpose_block(b)
        ans += f(bt)
        ans += 100*f(b)
    return ans
    # b1, b2 = bs
    # b1 = b1.split('\n')
    # b2 = b2.split('\n')
    # # b1_trans = []
    # # for c in range(len(b1[0])):
    # #     b1_trans.append([])
    # #     for r in range(len(b1)):
    # #         b1_trans[c].append(b1[r][c])
    # # b1_trans = [''.join(row) for row in b1_trans]
    # b1_trans = transpose_block(b1)
    # print('\n'.join(b1))
    # print('')
    # print('\n'.join(b1_trans))
    # ans += f(b1_trans) * 100 + f(b2)



    # return ans








if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    input = sys.stdin.read().strip()
    print('  ->', main(input) == (AOC_ANSWER[0], AOC_ANSWER[1]))


