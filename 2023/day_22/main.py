"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2
# 08:21:57
# 09:06:09

AOC_ANSWER = (477, None)

import sys
sys.path.append(AOC_BASE_PATH := '/'.join(__file__.replace('\\', '/').split('/')[:-3]))
from aoc_tools import print_function
import itertools as it
from dataclasses import dataclass, field
from collections import defaultdict
import re
import numpy as np
from pprint import pprint
from functools import cache
import math


def apply_gravity(bricks: list[tuple[int, int, int], tuple[int, int, int]]) -> int:
    bricks.sort(key=lambda x: min(x[0][2], x[1][2]))
    # Start fall simulation
    # Works but can be prettier. Also slow for input
    moves = 0
    for idx, brick in enumerate(bricks):
        # print(idx)
        # s, e = brick
        (sx, sy, sz), (ex, ey, ez) = brick
        dz = 0
        while sz + dz > 1:
            zz = sz + dz 
            for other_idx, other in enumerate(bricks[:idx]):
                z_collision = other[1][2] == (zz - 1)
                if not z_collision:
                    continue
                x_collision = sx <= other[0][0] <= ex or sx <= other[1][0] <= ex or other[0][0] <= sx <= other[1][0] or other[0][0] <= ex <= other[1][0]
                if not x_collision:
                    continue
                y_collision = sy <= other[0][1] <= ey or sy <= other[1][1] <= ey or other[0][1] <= sy <= other[1][1] or other[0][1] <= ey <= other[1][1]
                if not y_collision:
                    continue
                break
            else:
                dz -= 1
                continue
            break   
        moves += dz < 0      
        bricks[idx] = (sx, sy, sz+dz), (ex, ey, ez+dz)
    return moves


def has_moves(bricks) -> bool:
    # Start fall simulation
    # Works but can be prettier. Also slow for input
    moves = 0
    for idx, brick in enumerate(bricks):
        # print(idx)
        # s, e = brick
        (sx, sy, sz), (ex, ey, ez) = brick
        dz = 0
        while sz + dz > 1:
            zz = sz + dz 
            for other in bricks[:idx]:
                z_collision = other[1][2] == (zz - 1)
                if not z_collision:
                    continue
                x_collision = sx <= other[0][0] <= ex or sx <= other[1][0] <= ex or other[0][0] <= sx <= other[1][0] or other[0][0] <= ex <= other[1][0]
                if not x_collision:
                    continue
                y_collision = sy <= other[0][1] <= ey or sy <= other[1][1] <= ey or other[0][1] <= sy <= other[1][1] or other[0][1] <= ey <= other[1][1]
                if not y_collision:
                    continue
                break
            else:
                return True
            break     
    return False

@print_function
def part_one(input: str) -> int:
    lines = input.split('\n')
    bricks = []
    for line in lines:
        start, end = line.split('~')
        start = list(map(int, start.split(',')))
        end = list(map(int, end.split(',')))
        bricks.append((start, end))
        assert tuple(end) >= tuple(start), 'Start has lower values'
    bricks.sort(key=lambda x: min(x[0][2], x[1][2]))
    pprint(bricks)
    # Start fall simulation
    # Works but can be prettier. Also slow for input
    apply_gravity(bricks)
    pprint(bricks)
    ans = 0
    for idx, brick in enumerate(bricks):
        print(idx)
        # pprint(bricks)
        copy_bricks = bricks.copy()
        copy_bricks.remove(brick)
        moves = apply_gravity(copy_bricks)
        if moves == 0:
            ans += 1
    
    return ans
    # return len(lines)-len(supporting)











@print_function
def part_two(input: str) -> int:
    lines = input.split('\n')
# @print_function
# def main(input: str) -> tuple[int, int]:
#     return (part_one(input), part_two(input))
if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    input = sys.stdin.read().strip()
    print(part_one(input) == AOC_ANSWER[0])
    print(part_two(input) == AOC_ANSWER[1])
    # print('  ->', main(input) == (AOC_ANSWER[0], AOC_ANSWER[1]))


