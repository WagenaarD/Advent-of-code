"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (40, 241)

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
from pprint import pprint

MFCSAM = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1,
}

MFCSAM_2 = {
    'children': lambda x: x == 3,
    'cats': lambda x: x > 7,
    'samoyeds': lambda x: x == 2,
    'pomeranians': lambda x: x < 3,
    'akitas': lambda x: x == 0,
    'vizslas': lambda x: x == 0,
    'goldfish': lambda x: x < 5,
    'trees': lambda x: x > 3,
    'cars': lambda x: x == 2,
    'perfumes': lambda x: x == 1,
}


@print_function
def main(input: str) -> tuple[int, int]:
    p1, p2 = 0, 0
    for idx, line in enumerate(input.split('\n'), 1):
        if all(MFCSAM[key] == int(val) for key, val in re.findall('(\\w+): (\\d+)', line)):
            p1 = idx
        if all(MFCSAM_2[key](int(val)) for key, val in re.findall('(\\w+): (\\d+)', line)):
            p2 = idx        
    return p1, p2

aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')


