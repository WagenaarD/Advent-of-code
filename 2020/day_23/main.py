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

AOC_ANSWER = (None, None)

def cup_move(cups: list[int]):
    picked_up = [cups.pop(1) for _ in range(3)]
    print(f'{cups=}')
    print(f'{picked_up=}')
    sorted_cups = list(sorted(cups))
    print(f'{sorted_cups=}')
    dest = sorted_cups[sorted_cups.index(cups[0])-1]
    print(f'{dest=}')
    dest_idx = cups.index(dest)
    print(f'{dest_idx=}')
    cups = cups[:dest_idx] + picked_up + cups[dest_idx]


@print_function
def part_one(input_txt: str) -> int:
    cups = list(map(int, list(input_txt)))
    print(f'{cups=}')
    cups = cup_move(cups)
    








@print_function
def part_two(input_txt: str) -> int:
    lines = input_txt.split('\n')
@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        part_one(input_txt), 
        part_two(input_txt)
    )

aoc_run( __name__, __file__, main, AOC_ANSWER)
