"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

AOC_ANSWER = (36758, 76358113886726)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import itertools as it
import re
from fractions import Fraction

PART_2_INCREMENT = 10000000000000

@print_function
def part_one(input_txt: str) -> int:
    """
    Old
    Calculates the number of required A and B button presses and the corresponding coin cost. The 
    cost of an A-press is 3 and B-press is 1. No more than 100 presses are allowed per button.
    If no solution is possible, 0 cost is stored.
    """
    input_blocks = input_txt.split('\n\n')
    p1 = 0
    for block in input_blocks:
        ax, ay, bx, by, px, py = map(int, re.findall('-?\\d+', block))
        costs = []
        for a_count, b_count in it.product(range(101), repeat=2):
            target_x = ax * a_count + bx * b_count
            target_y = ay * a_count + by * b_count
            if target_x == px and target_y == py:
                costs.append(3*a_count + b_count)
        if costs:
            p1 += min(costs)
    return p1


@print_function
def solve(input_txt: str, increment: int, max_steps: int) -> int:
    """
    Analytical solver for the required number of button presses.

    When numbers get large, float errors can occur. That's why I use Fraction which is exact even 
    though it is slower.
    
    Quickest way to the answer is using:
        px = ax*A + bx*B (1)
        py = ay*A + by*B (2)
        A = (px-bx*B)/ax (3)
    Inserting (3) into (2) gives:
        ay*(px-bx*B)/ax + by*B = py
        ay*px/ax-ay*bx/ax*B+by*B = py
        (by-aybx/ax)*B=py-ay*px/ax
        B = (py-ay*px/ax)/(by-ay*bx/ax)
        B = (ax*py-ay*px)/(ax*by/ay*bx) (4)
    Similarly, one gets:
        A = (ax*py-ay*px)/(ax*by-ay*bx) (5)
    """
    ans = 0
    for block in input_txt.split('\n\n'):
        ax, ay, bx, by, px, py = map(int, re.findall('-?\\d+', block))
        px += increment
        py += increment
        # Using math we can find the answer directly
        a_steps = Fraction(bx*py-by*px, ay*bx-ax*by)
        b_steps = Fraction(ax*py-ay*px, ax*by-ay*bx)
        # We can only take integer steps and they should be positive
        valid = all(step <= max_steps for step in (a_steps, b_steps)) if max_steps else True
        if valid and all(step.is_integer() and step >= 0 for step in (a_steps, b_steps)):
            ans += int(round(3*a_steps + b_steps))
    return ans


@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        solve(input_txt, 0, 100),
        solve(input_txt, PART_2_INCREMENT, None),
    )
aoc_run(__name__, __file__, main, AOC_ANSWER)


