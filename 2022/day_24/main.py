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
import itertools as it
from dataclasses import dataclass, field
from collections import defaultdict
import re
import numpy as np
from pprint import pprint
from functools import cache
from datetime import datetime


DIRS = {
    '>': ( 0,  1),
    '<': ( 0, -1),
    '^': (-1,  0),
    'v': ( 1,  0),
}
MOVES = ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1))


def print_grid(blizzards, start, end, width, height, stack = []):
    """
    Visualize the grid similarly to the example output. Add an 'E' to every coordinate present in 
    stack
    """
    for row in range(-1, height + 1):
        output = '■'
        for col in range(width):
            blizs = [bliz for bliz in blizzards if (row, col) == (bliz[0], bliz[1])]
            if len(blizs) > 1:
                output += str(len(blizs))
            elif len(blizs) == 1:
                output += blizs[0][2]
            elif (row, col) in stack:
                output += 'E'
            elif (row, col) in (start, end):
                output += '.'
            elif row in (-1, height):
                output += '■'
            else:
                output += '.'
        print(output + '■')
    print('')


def move_blizzards(blizzards, width, height):
    new_blizzards = []
    for row, col, dir in blizzards:
        drow, dcol = DIRS[dir]
        nrow, ncol = (row + drow) % height, (col + dcol) % width
        new_blizzards.append((nrow, ncol, dir))
    return new_blizzards


@print_function()
def bfs(blizzards, start, end, width, height):
    t = 0
    stack = {start}
    if width < 10: print_grid(blizzards, start, end, width, height, stack)
    while len(stack) >= 1:
        if width < 10: print('== Minute {}, stack {} =='.format(t, stack))
        if width < 10: print_grid(blizzards, start, end, width, height, stack)
        t += 1
        blizzards = move_blizzards(blizzards, width, height)
        blizzard_locations = {(bliz[0], bliz[1]) for bliz in blizzards}
        old_stack = stack
        stack = set()
        for row, col in old_stack:
            for drow, dcol in MOVES:
                nrow, ncol = row + drow, col + dcol
                if (nrow, ncol) == end:
                    return (t, blizzards)
                if 0 <= nrow < height and 0 <= ncol < width or (nrow, ncol) == start:
                    if (nrow, ncol) not in blizzard_locations:
                        stack.add((nrow, ncol))
                        

if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    lines = sys.stdin.read().strip().split('\n')
    # Blizzards in grid starting at [0][0]
    start = (-1, lines[0].index('.') - 1)
    end = (len(lines) - 2, lines[-1].index('.') - 1)
    width = len(lines[0])-2
    height = len(lines) - 2
    blizzards = []
    for row, line in enumerate(lines[1:-1]):
        for col, char in enumerate(line[1:-1]):
            if char != '.':
                blizzards.append((row, col, char))

    t_0, blizzards = bfs(blizzards, start, end, width, height)
    t_1, blizzards = bfs(blizzards, end, start, width, height)
    t_2, blizzards = bfs(blizzards, start, end, width, height)
    print('Part 1:', t_0)
    print('Part 2:', t_0 + t_1 + t_2)