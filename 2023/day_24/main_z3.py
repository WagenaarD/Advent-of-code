"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
# python3 main.py < in
pypy3 main.py

Original solution, but using z3 feels like cheating so not considered my 'main' solutions
"""
# Start, Part 1, Part 2
# 12:39:23
# 13:09:22
# 16:38:26 # Did other things in between

AOC_ANSWER = (13149, 1033770143421619)

import sys
sys.path.append(AOC_BASE_PATH := '/'.join(__file__.replace('\\', '/').split('/')[:-3]))
from aoc_tools import print_function, aoc_run, print_loop
import itertools as it
import re
import numpy as np
from functools import cache
import math
import z3
import matplotlib.pyplot as plt

TOLERANCE = 1E-10


@print_function
def part_one(input: str) -> int:
    lines = input.split('\n')
    hail = []
    for line in lines:
        nums = list(map(int, re.findall('-?\d+', line)))
        hail.append((tuple(nums[:3]), tuple(nums[3:])))
    
    lower = 200000000000000
    upper = 400000000000000
    if is_example := (len(hail) < 10): lower, upper = 7, 27
    ans = 0
    for idx, (pos1, vel1) in enumerate(hail):
        for pos2, vel2 in hail[idx+1:]:
            assert (pos1, vel1) != (pos2, vel2)
            # print(f'\nHailstone A: {pos1} @ {vel1}')
            # print(f'Hailstone B: {pos2} @ {vel2}')
            # try:
            b1 = vel1[1] / vel1[0]
            a1 = pos1[1] - pos1[0] * b1
            b2 = vel2[1] / vel2[0]
            a2 = pos2[1] - pos2[0] * b2
            if b1 == b2:
                # print("Hailstones' paths are parallel; they never intersect.")
                continue
            x = (a1 - a2) / (b2 - b1)
            y = a1 + b1 * x
            t1 = (x-pos1[0])/vel1[0]
            t2 = (x-pos2[0])/vel2[0]
            in_test = lower <= x <= upper and lower <= y <= upper
            # if lower <= x <= upper and lower <= y <= upper:
            #     ans +=1 
            if t1 < 0 and t2 < 0:
                pass
                # print("Hailstones' paths crossed in the past for both hailstones.")
            if t1 < 0:
                pass
                # print("Hailstones' paths crossed in the past for hailstone A.")
            elif t2 < 0:
                pass
                # print("Hailstones' paths crossed in the past for hailstone B.")
            elif in_test:
                # print("Hailstones' paths will cross inside the test area (at x={}, y={}).".format(x, y))
                ans += 1
            else:
                pass
                # print("Hailstones' paths will cross outside the test area.")
    return ans

            
@print_function
def part_two(input: str) -> int:
    lines = input.split('\n')
    hail = []
    for line in lines:
        nums = list(map(int, re.findall('-?\d+', line)))
        hail.append((tuple(nums[:3]), tuple(nums[3:])))
    # Put all arguments in z3 which will solve it for us. This feels like cheating. Partly because
    # Tamara told me that others solved today using z3 which put me on this track.
    Xso = z3.Real('Xso')
    Yso = z3.Real('Yso')
    Zso = z3.Real('Zso')
    Vxs = z3.Real('Vxs')
    Vys = z3.Real('Vys')
    Vzs = z3.Real('Vzs')
    Ps = [Xso, Yso, Zso]
    Vs = [Vxs, Vys, Vzs]
    solver = z3.Solver()
    for idx, (Pi, Vi) in enumerate(hail):
        Ti = z3.Real(f'T{idx}')
        # solver.add(Ti > 0)
        for ax in range(3):
            solver.add(Pi[ax] + Vi[ax] * Ti == Ps[ax] + Vs[ax] * Ti)
    assert solver.check() == z3.sat
    model = solver.model()
    return sum(model[arg].as_long() for arg in (Xso, Yso, Zso))


@print_function
def main(input: str) -> tuple[int, int]:
    return (
        part_one(input), 
        part_two(input),
    )

aoc_run( __name__, __file__, main, AOC_ANSWER, 'in')
# aoc_run(__name__, __file__, main, AOC_ANSWER, 'ex')


