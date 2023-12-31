"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (None, None)

import sys
sys.path.append(AOC_BASE_PATH := '/'.join(__file__.replace('\\', '/').split('/')[:-3]))
from aoc_tools import print_function, aoc_run
import itertools as it
from dataclasses import dataclass, field
from collections import defaultdict, deque
import re
import numpy as np
from pprint import pprint
from functools import cache
import math


@print_function
def part_one(input: str) -> int:
    lines = input.split('\n')







@print_function
def part_two(input: str) -> int:
    lines = input.split('\n')
@print_function
def main(input: str) -> tuple[int, int]:
    return (
        part_one(input), 
        part_two(input)
    )
aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')


