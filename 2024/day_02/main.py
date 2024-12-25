"""
Advent of code challenge
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (279, 343)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run


def is_safe(report : 'list[str]') -> bool:
    ## Tamara did this, which I find more elegant. It is also faster (5ms vs 9ms)
    # report_differences = {n2-n1 for n1, n2 in zip(report, report[1:])}
    # return report_differences <= {1, 2, 3} or report_differences <= {-1, -2, -3}
    ##  My original code
    signs, diffs = set(), []
    for n1, n2 in zip(report, report[1:]):
        diffs.append(abs(n2-n1))
        if diffs[-1] == 0:
            signs.add(0)
        else:
            signs.add((n2-n1)/diffs[-1])
    return len(signs) == 1 and min(diffs) >= 1 and max(diffs) <= 3


@print_function
def main(input: str) -> tuple[int, int]:
    p1, p2 = 0, 0
    for line in input.split('\n'):
        report = list(map(int, line.split()))
        p1 += is_safe(report)
        for idx in range(len(report)):
            if is_safe(report[:idx] + report[idx+1:]):
                p2 += 1
                break
    return p1, p2
    
    

aoc_run( __name__, __file__, main, AOC_ANSWER, 'in')


