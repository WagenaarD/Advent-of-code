"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2
# 13:52:06
# 14:19:59
# 

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

DIRS = {
    '>': ( 0,  1),
    '<': ( 0, -1),
    '^': (-1,  0),
    'v': ( 1,  0),
}


@print_function()
def main(input: str) -> int:
    grid = input.split('\n')
    seen_states = set()
    new_beams = [(0,-1,'>')]
    while new_beams:
        beams = new_beams
        new_beams = []
        for r, c, dir in beams:
            # new_beams = []
            dr, dc = DIRS[dir]
            rr, cc = r + dr, c + dc
            out_of_bounds = not (0 <= rr < len(grid) and 0 <= cc < len(grid[0]))
            if out_of_bounds:
                continue
            char = grid[rr][cc]
            print(rr, cc, char)
            if char == '.':
                new_beams.append((rr, cc, dir))
            elif char == '|':
                if dir in ('><'):
                    new_beams.append((rr, cc, '^'))
                    new_beams.append((rr, cc, 'v'))
                else:
                    new_beams.append((rr, cc, dir))
            elif char == '-':
                if dir in ('v^'):
                    new_beams.append((rr, cc, '<'))
                    new_beams.append((rr, cc, '>'))
                else:
                    new_beams.append((rr, cc, dir))
            elif char == '/':
                if dir == '>':
                    new_beams.append((rr, cc, '^'))
                elif dir == '^':
                    new_beams.append((rr, cc, '>'))
                if dir == '<':
                    new_beams.append((rr, cc, 'v'))
                elif dir == 'v':
                    new_beams.append((rr, cc, '<'))
            elif char == '\\':
                if dir == '>':
                    new_beams.append((rr, cc, 'v'))
                elif dir == 'v':
                    new_beams.append((rr, cc, '>'))
                if dir == '<':
                    new_beams.append((rr, cc, '^'))
                elif dir == '^':
                    new_beams.append((rr, cc, '<'))
            else:
                assert False, 'Unhandled char'
        print('new_beams (before filtering)', new_beams)
        new_beams = [beam for beam in new_beams if not beam in seen_states]
        print('new_beams (after filtering)', new_beams)
        for beam in new_beams:
            seen_states.add(beam)
    
    print(seen_states)
    seen_pos = [(r, c) for r, c, _ in seen_states]
    for r, row in enumerate(grid):
        print(''.join(['#' if (r,c) in seen_pos else '.' for c, _ in enumerate(row)]))
    
    return len(set(seen_pos))
                


        
            













if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    input = sys.stdin.read().strip()
    print('  ->', main(input) == (AOC_ANSWER[0], AOC_ANSWER[1]))


