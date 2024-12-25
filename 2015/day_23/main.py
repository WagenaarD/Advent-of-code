"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (255, 334)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run


def solve(input_txt: str, reg: dict) -> int:
    lines = input_txt.replace(',', '').split('\n')

    idx = 0
    while idx < len(lines):
        lp = lines[idx].split()
        # print(lp, reg)
        # hlf r sets register r to half its current value, then continues with the next instruction.
        if lp[0] == 'hlf':
            reg[lp[1]] //= 2
        # tpl r sets register r to triple its current value, then continues with the next instruction.
        if lp[0] == 'tpl':
            reg[lp[1]] *= 3
        # inc r increments register r, adding 1 to it, then continues with the next instruction.
        if lp[0] == 'inc':
            reg[lp[1]] += 1
        # jmp offset is a jump; it continues with the instruction offset away relative to itself.
        if lp[0] == 'jmp':
            idx += int(lp[1]) - 1
        # jie r, offset is like jmp, but only jumps if register r is even ("jump if even").
        if lp[0] == 'jie':
            if reg[lp[1]] % 2 == 0:
                idx += int(lp[2]) - 1
        # jio r, offset is like jmp, but only jumps if register r is 1 ("jump if one", not odd).
        if lp[0] == 'jio':
            if reg[lp[1]] == 1:
                idx += int(lp[2]) - 1
        idx += 1
    return reg['b']


@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        solve(input_txt, {'a': 0, 'b': 0}), 
        solve(input_txt, {'a': 1, 'b': 0})
    )

aoc_run( __name__, __file__, main, AOC_ANSWER)
