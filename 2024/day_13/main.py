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
def part_two(input_txt: str, increment: int = PART_2_INCREMENT, max_steps = None) -> int:
    """
    Analytical solver for the required number of button presses.
    For each A (ax, ay) and B (bx, by) there are a C (cx, cy=0) and D (dx=0, dy) which are expressed 
    as linear functions of A and B with cy = 0 and dx = 0. It is easy to find the number of button 
    presses of C and D which can then be used to calculate button presses of A and B.
    When numbers get large, float errors can occur. That's why I use Fraction which is exact even 
    though it is slower.
    """
    input_blocks = input_txt.split('\n\n')
    ans = 0
    for block in input_blocks:
        ax, ay, bx, by, px, py = map(int, re.findall('-?\\d+', block))
        px += increment
        py += increment
        ## Define C and D along the x-axis and y-axis respectively
        # C = A - ay/by * B
        # D = A - ax/bx * B
        cx = ax - Fraction(ay*bx, by)
        dy = ay - Fraction(ax*by, bx)
        c_steps = px / cx
        d_steps = py / dy
        # Calculate a_steps from the sum of c and d, then calculate b_steps using the residual x.
        a_steps = c_steps + d_steps
        b_steps = (c_steps * cx - a_steps * ax) / bx
        # We can only take integer steps and they should be positive
        valid = all(step.is_integer() and step > 0 for step in (a_steps, b_steps))
        if max_steps:
            valid = valid and all(step < max_steps for step in (a_steps, b_steps))
        if valid:
            ans += int(round(3*a_steps + b_steps))
    return ans


@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        part_one(input_txt), 
        # part_two(input_txt, 0, 100), # = part one 
        part_two(input_txt),
    )
aoc_run(__name__, __file__, main, AOC_ANSWER)


