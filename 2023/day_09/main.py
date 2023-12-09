"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2
# 08:14:39
# 08:46:41 -teken vergeten bij regex, anders klaar na 8 min.
# 11:23:22 met pauze

AOC_ANSWER = (1702218515, 925)

import sys
sys.path.append('../..')
from aoc_tools import print_function

@print_function()
def main(input: str) -> 'tuple(int, int)':
    score_p1, score_p2 = 0, 0
    for line in input.split('\n'):
        deriv_lines = [list(map(int, line.split()))]
        while not all(num == 0 for num in deriv_lines[-1]):
            deriv_lines.append([n2-n1 for n1, n2 in zip(deriv_lines[-1], deriv_lines[-1][1:])])
        # These two lines replace the rest of the code but are slightly slower and more complex:
        # score_p1 += sum([deriv[-1] for deriv in deriv_lines])
        # score_p2 += sum([(-1)**idx * deriv[0] for idx, deriv in enumerate(deriv_lines)])
        extra_last = 0
        extra_first = 0
        for deriv in deriv_lines[::-1]:
            extra_last += deriv[-1]
            extra_first = deriv[0] - extra_first
        score_p1 += extra_last
        score_p2 += extra_first
    return (score_p1, score_p2)


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    input = sys.stdin.read().strip()
    print('  ->', main(input) == (AOC_ANSWER[0], AOC_ANSWER[1]))

