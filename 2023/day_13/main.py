"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2
# 06:01:30
# 06:53:43

AOC_ANSWER = (34772, 35554)

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



def find_horizontals(b: str, factor = 1) -> 'list[int]':
    """
    Finds all horizontal mirror lines
    """    
    b = b.split('\n')
    out = []
    for idx in range(1, len(b)):
        up = list(reversed(b[:idx]))
        down = b[idx:]
        sz = min(len(up), len(down))
        valid = ''.join(up[:sz]) == ''.join(down[:sz])
        if valid:
            out.append(idx)
    return out


def transpose_block(b: str) -> str:
    """
    Transposes the block. 
    """
    b = [list(r) for r in b.split('\n')]
    bt = [[''] * len(b) for idx in range(len(b[0]))]    
    for r, row in enumerate(b):
        for c, char in enumerate(row):
            bt[c][r] = char
    return '\n'.join([''.join(row) for row in bt])


def block_scores(b: str) -> 'list[int]':
    """
    Returns a list of possible scores for various horizontal and vertical lines.
    """
    return [num * 100 for num in find_horizontals(b)] + find_horizontals(transpose_block(b))


def print_block_line(b, idx = -1, transpose = False):
    """
    Only serves visualization purposes
    """
    if transpose:
        b = transpose_block(b)
    for line_idx, line in enumerate(b.split('\n'), 1):
        if line_idx == idx:
            print(f'{line_idx:3} {line}')
            print('-' * (len(line)+6))
        else:
            print(f'{line_idx:3} {line}')

@print_function()
def part_one(input: str) -> int:
    return sum(sum(block_scores(b)) for b in input.split('\n\n'))


@print_function()
def part_two(input: str) -> int:
    bs = input.split('\n\n')
    ans = 0
    for b_idx, b in enumerate(bs):
        base_scores = block_scores(b)
        # print(f'\n{b_idx}: Start')
        # print_block_line(b)
        # print('')
        print_block_line(b, -1, True)
        for idx, char in enumerate(b):
            if char == '\n':
                continue
            new_char = '#' if char == '.' else '.'
            new_b = b[:idx] + new_char + b[idx+1:]
            new_scores = [score for score in block_scores(new_b) if score not in base_scores]
            if new_scores:
                assert len(new_scores) == 1, 'Len should be one'
                # if new_scores[0] % 100 == 0:
                #     print(f'\n{b_idx}: {new_scores[0]} - Horizontal line')
                #     print_block_line(new_b, new_scores[0] // 100, True)
                # else:
                #     print(f'\n{b_idx}: {new_scores[0]} - Vertical line')
                #     print_block_line(new_b, new_scores[0])
                ans += sum(new_scores)
                break
        else:
            assert False, f'No solution for {b_idx}'
    return ans


def main(input: str) -> 'tuple(int, int)':
    return (part_one(input), part_two(input))


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    input = sys.stdin.read().strip()
    print('  ->', main(input) == (AOC_ANSWER[0], AOC_ANSWER[1]))


