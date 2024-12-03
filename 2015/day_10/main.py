"""
Advent of code challenge
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (492982, 6989950)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import re


def look_and_say(seq: str) -> str:
    new_seqs = []
    for mtch in re.findall('|'.join(f'{d}+' for d in '0123456789'), seq):
        new_seqs.append(str(len(mtch)) + mtch[0])
    return ''.join(new_seqs)
    

@print_function
def main(input: str) -> tuple[int, int]:
    for _ in range(40):
        input = look_and_say(input)
    p1 = len(str(input))
    for _ in range(10):
        input = look_and_say(input)
    p2 = len(str(input))
    return p1, p2


aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')


