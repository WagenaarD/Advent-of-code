"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2
# Forgot
# 09:27:24


AOC_ANSWER = (506891, None)

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


@print_function()
def main(input: str) -> int:
    steps = input.split(',')
    # print(steps)
    ans = 0 
    for idx, step in enumerate(steps):
        value = 0
        for ch in step:
            value += ord(ch)
            value *= 17
            value %= 256
        print(f'{idx:4} {step:10} {value:5}')
        ans += value
    return ans



            






if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    input = sys.stdin.read().strip()
    # main('HASH')
    print('  ->', main(input) == (AOC_ANSWER[0], AOC_ANSWER[1]))


