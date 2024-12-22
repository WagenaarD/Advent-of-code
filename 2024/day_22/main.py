"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
from collections import defaultdict


AOC_ANSWER = (17960270302, 2042)

def next_secret(secret: int) -> int:
    """
    To calculate the next secret, there are three steps which are each followed by "mixing" and 
    "pruning". Mixing is taking the bitwise XOR with the previous number and pruning is taking the 
    modulus of 16777216 (=2**24).
    The three steps are multiply with 64, floordivide by 32 and multiply with 2048
    """
    secret ^= secret * 64
    secret %= 16777216
    secret ^= secret // 32
    secret %= 16777216
    secret ^= secret * 2048
    secret %= 16777216
    return secret


@print_function
def main(input_txt: str) -> tuple[int, int]:
    """
    For each initial number, calculate the next 2000 numbers. For p1, add the last number to the 
    score. For p2, keep track of the pattern, defined as the last four differences, and add the 
    sell-price for that pattern to a dictionary the first time it occurs.
    """
    initial_numbers = list(map(int, input_txt.split('\n')))
    p1 = 0
    p2_scores = defaultdict(int)
    for current in initial_numbers:
        differences = []
        seen = set()
        for idx in range(2000):
            previous, current = current, next_secret(current)
            differences.append(current%10 - previous%10)
            if idx < 4:
                continue
            last_four = tuple(differences[-4:])
            if last_four not in seen:
                seen.add(last_four)
                p2_scores[last_four] += current%10
        p1 += current
    return p1, max(p2_scores.values())

aoc_run(__name__, __file__, main, AOC_ANSWER)
