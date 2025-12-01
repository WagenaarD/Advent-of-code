"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run

AOC_ANSWER = (1086, 6268)

@print_function
def main(input_txt: str) -> int:
    lines = input_txt.split('\n')
    dial = 50
    score_p1, score_p2 = 0, 0
    for line in lines:
        d = 1 if line[0] == 'R' else -1
        num = int(line[1:])
        score_p2 += num // 100
        num %= 100
        for _ in range(num):
            dial += d
            dial %= 100
            if dial == 0:
                score_p2 += 1
        if dial == 0:
            score_p1 += 1
    return score_p1, score_p2

aoc_run( __name__, __file__, main, AOC_ANSWER)
