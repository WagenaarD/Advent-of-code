"""
From year folder:
../aoc_tools/aoc_start.sh xx && cd day_xx

Advent of code challenge
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (664, 640)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import itertools as it
from collections import defaultdict


def find_best_score(score_chart):
    best_score = 0
    for order in it.permutations(score_chart.keys()):
        order = list(order) + [order[0]]
        score = 0
        for name_1, name_2 in zip(order, order[1:]):
            score += score_chart[name_1][name_2] + score_chart[name_2][name_1]
        best_score = max(best_score, score)
    return best_score

@print_function
def main(input: str) -> tuple[int, int]:
    lines = input.split('\n')
    score_chart = defaultdict(dict)
    for line in lines:
        name_1, _, sign, num, _, _, _, _, _, _, name_2 = line[:-1].split()
        score_chart[name_1][name_2] = (1 if sign == 'gain' else -1) * int(num)
    p1 = find_best_score(score_chart)
    for name in list(score_chart.keys()):
        score_chart['me'][name], score_chart[name]['me'] = 0, 0
    p2 = find_best_score(score_chart)
    return p1, p2

    
aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')


