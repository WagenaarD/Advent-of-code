"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# 06:00:00
# 06:35:18
# 07:50:00

AOC_ANSWER = (7286, 25470469710341)

import sys
sys.path.append('../..')
from aoc_tools import print_function
import re
from functools import cache
import itertools as it

@cache
def possible_solutions(bprint: str, score: 'tuple[int]') -> int:
    # Pruning
    if sum(score) + len(score) + 1 > len(bprint):
        return 0
    # Scoring
    if not score:
        if bprint.count('#') == 0:
            return 1
        else:
            return 0
    # Branching
    val = score[0]
    new_score = score[1:]
    ans = 0
    match_string = '(?=([.?][#?]{' + str(val) + '}[.?]))'
    for mtch in re.finditer(match_string, bprint):
        if not mtch:
            continue
        if '#' in bprint and mtch.start()+1 > bprint.find('#'):
            continue
        end = mtch.start() + val
        new_bprint = bprint[end+2:] 
        ans += possible_solutions('.' + new_bprint, new_score)
    return ans


@print_function()
def solve(input: str, factor: int = 5) -> int:
    lines = input.split('\n')
    ans = 0
    for line in lines:
        bprint, vals = line.split()
        bprint = '?'.join([bprint] * factor)
        vals = ','.join([vals] * factor)
        score = tuple(int(num) for num in vals.split(','))
        ans += possible_solutions('.' + bprint + '.', score)
    return ans


def main(input: str) -> 'tuple(int, int)':
    return (solve(input, 1), solve(input, 5))

@print_function()
def part_one_in_one_line(input: str) -> int:
    return sum([tuple(len(block) for block in re.findall('#+', ''.join([val for pair in zip(bprint.split('?'), chars) for val in pair]) + bprint.split('?')[-1])) == tuple(map(int, vals.split(','))) for bprint, vals in [line.split() for line in input.split('\n')] for chars in it.product('#.', repeat = bprint.count('?'))])

if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    input = sys.stdin.read().strip()
    print('  ->', main(input) == (AOC_ANSWER[0], AOC_ANSWER[1]))
    print('  ->', part_one_in_one_line(input) == AOC_ANSWER[0])


