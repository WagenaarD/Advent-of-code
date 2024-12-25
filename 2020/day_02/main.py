"""
Advent of code challenge
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (572, 306)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
from aoc_tools import print_loop
import itertools as it
from dataclasses import dataclass, field
from collections import defaultdict, deque
import re
import numpy as np
from pprint import pprint
from functools import cache
import math


@print_function
def main(input: str) -> int:
    lines = input.split('\n')
    p1, p2 = 0, 0
    for line in lines:
        # example input line = "1-3 a: abcde"
        n1, n2, chr, password = re.match('(\\d+)-(\\d+) (\\w): (\\w+)', line).groups()
        n1, n2 = int(n1), int(n2)
        p1 += n1 <= password.count(chr) <= n2
        p2 += (password[n1-1] == chr) != (password[n2-1] == chr)
    return p1, p2

aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')


