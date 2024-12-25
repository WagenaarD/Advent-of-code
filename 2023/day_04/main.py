"""
Advent of code challenge 2023
>> python3 main.py < in
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2
# 07:59:34
# 08:04:15
# 08:13:14  13:40   07:08

import sys
sys.path.append(AOC_BASE_PATH := '/'.join(__file__.replace('\\', '/').split('/')[:-3]))
from aoc_tools import print_function, aoc_run

AOC_ANSWER = (21485, 11024379)

@print_function
def main(input: str) -> tuple[int, int]:
    lines = input.strip().split('\n')
    score_p1, score_p2 = 0, [1] * len(lines)
    for idx, line in enumerate(lines):
        left, right = line.split(': ')[1].split('|')
        correct = len(set(left.split()) & set(right.split()))
        if correct:
            score_p1 += 2 ** (correct - 1)
        for idx2 in range(idx+1, idx+correct+1):
            score_p2[idx2] += score_p2[idx]
    return score_p1, sum(score_p2)

aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')
