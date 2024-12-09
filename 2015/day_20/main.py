"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (831600, 884520)

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
from functools import cache, reduce
import math
from pprint import pprint


def get_score_p1(idx):
    return sum(10*idx2 if idx % idx2 == 0 else 0 for idx2 in range(1, idx+1))


@print_function
def part_one(input: str) -> int:
    target = int(input)
    idx = 1
    scores = defaultdict(int)
    upper_limit = 1
    while get_score_p1(upper_limit) < target:
        upper_limit *= 2
    print(f'{upper_limit=:,}')
    for idx in range(1, upper_limit):
        steps = 1
        while steps*idx < upper_limit:
            scores[idx*steps] += 10*idx
            steps += 1
    p1 = min([key for key, score in scores.items() if score > target])
    return p1


@print_function
def part_two(input: str) -> int:
    target = int(input)
    scores = defaultdict(int)
    max_score = 0
    for idx in it.count(1):
        for steps in range(1, 50):
            scores[idx*steps] += 11 * idx
        if scores[idx] > target:
            return idx
        max_score = max(max_score, scores[idx])
        
@print_function
def main(input: str) -> tuple[int, int]:
    return (
        part_one(input), 
        part_two(input)
    )
aoc_run(__name__, __file__, main, AOC_ANSWER)


