"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (None, None)

import sys
sys.path.append('..')
from aoc_tools import *
import itertools as it
from dataclasses import dataclass, field
from collections import defaultdict
import re
import numpy as np
from pprint import pprint
from functools import cache
import math


@print_function()
def part_one(lines):
    pass

if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    input = sys.stdin.read().strip()
    lines = sys.stdin.read().strip().split('\n')
    part_one(lines)

    # print('  ->', main(input) == (AOC_ANSWER[0], AOC_ANSWER[1]))


