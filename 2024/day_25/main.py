"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
from aoc_tools import print_loop, tuple_add, tuple_sub, tuple_mult, Pos
import itertools as it
from dataclasses import dataclass, field
from collections import defaultdict, deque, Counter
import re
import numpy as np
from pprint import pprint
from functools import cache, reduce
import math
from pprint import pprint
import heapq

AOC_ANSWER = (2835, None)


@print_function
def part_one(input_txt: str) -> int:
    """
    Schematics are split by \n\n and consist of lines of length 5, lock schematics start with a line
    of # (and keys are the other way around). I count the number of # per column, then check whether
    the sum per column for each lock-key combination exceeds the maximum (5).
    """
    locks = []
    keys = []
    for schematic in input_txt.split('\n\n'):
        lines = schematic.split('\n')
        is_key = lines[-1] == '#####'
        if is_key:
            lines = lines[::-1]
        chars = [-1] * 5
        for c in range(len(lines[0])):
            for r in range(len(lines)):
                if lines[r][c] == '#':
                    chars[c] += 1
                else:
                    break
        if is_key:
            keys.append(chars)
        else:
            locks.append(chars)
    ans = 0
    for lock in locks:
        for key in keys:
            for column in range(5):
                if lock[column] + key[column] > 5:
                    break
            else:
                ans += 1
    return ans


@print_function
def part_two(input_txt: str) -> int:
    return

@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        part_one(input_txt), 
        part_two(input_txt)
    )

aoc_run( __name__, __file__, main, AOC_ANSWER)
