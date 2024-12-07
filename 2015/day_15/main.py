"""
Advent of code challenge
python3 main.py < in
"""

AOC_ANSWER = (18965440, 15862900)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import itertools as it
import re
import math


@print_function
def main(input: str) -> tuple[int, int]:
    ingredient_lst = [list(map(int, re.findall('-?\\d+', line))) for line in input.split('\n')]
    p1, p2 = 0, 0
    for comb in it.combinations_with_replacement(list(range(len(ingredient_lst))), 100):
        scores = [0] * len(ingredient_lst[0])
        for idx, ingredient in enumerate(ingredient_lst):
            count = comb.count(idx)
            for idx_2 in range(len(scores)):
                scores[idx_2] += ingredient[idx_2] * count
        if any(score < 0 for score in scores):
            continue
        total_score = math.prod(scores[:-1])
        p1 = max(p1, total_score)
        if scores[-1] == 500:
            p2 = max(p2, total_score)
    return p1, p2

aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')


