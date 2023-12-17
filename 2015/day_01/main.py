"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (74, 1795)

import sys
sys.path.append('../..')
from aoc_tools import print_function
import itertools as it
from dataclasses import dataclass, field
from collections import defaultdict
import re
import numpy as np
from pprint import pprint
from functools import cache
import math


def part_one(input: str) -> int:
    return input.count('(') - input.count(')')


def part_two(input: str) -> int:
    pos = 0
    for idx, char in enumerate(input, 1):
        if char == '(':
            pos += 1
        else:
            pos -= 1
        if pos == -1:
            return idx


@print_function()
def main(input: str) -> tuple[int, int]:
    return (part_one(input), part_two(input))


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    input = sys.stdin.read().strip()
    print('  ->', main(input) == (AOC_ANSWER[0], AOC_ANSWER[1]))


