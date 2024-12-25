"""
Advent of code challenge
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (282749, 9962624)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
from aoc_tools import print_loop
import itertools as it
from dataclasses import dataclass, field
from collections import defaultdict, deque, Counter
import re
import numpy as np
from pprint import pprint
from functools import cache
import math
from hashlib import md5

def get_index(input: str, zeros: int) -> int:
    idx = 0
    while not md5((input + str(idx)).encode()).hexdigest().startswith('0' * zeros):
        idx += 1
    return idx


@print_function
def part_one(input: str) -> int:
    return get_index(input, 5)

@print_function
def part_two(input: str) -> int:
    return get_index(input, 6)

@print_function
def main(input: str) -> tuple[int, int]:
    return (
        part_one(input), 
        part_two(input)
    )

aoc_run( __name__, __file__, main, AOC_ANSWER, 'in')


