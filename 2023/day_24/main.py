"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
# python3 main.py < in
pypy3 main.py
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


UNIT_VECTOR_FINAL_TOLERANCE = 1E-8 # Gives good results if 1E-2, but better to be safe


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


def get_unit_vector(vector: tuple[float, float, float]) -> tuple[float, float, float]:
    """Scales the vector so that its lengths is equal to 1.0"""
    sqrt_sq_sum = math.sqrt(sum(vs**2 for vs in vector))
    return tuple(v/sqrt_sq_sum for v in vector)


@cache
def direction_error_cost(throw_dir: tuple) -> float:
    if sum(map(abs, throw_dir)) == 0: return 1e30
    throw_dir = get_unit_vector(throw_dir)
    if abs(throw_dir[2]) > 0.999: return 1e30
    isecs = get_intersections(throw_dir)
    ans = 0
    for i,j in ((0,1), (1,2), (0,2)):
        ans += (isecs[i]['uvw'][1] - isecs[j]['uvw'][1])**2
        ans += (isecs[i]['uvw'][2] - isecs[j]['uvw'][2])**2
    return ans


def get_intersections(throw_dir: tuple) -> list[dict]:
    """
    Calculates the position of all intersections in a 2D perspective defined by the argument as a 
    unit vector
    """
    u = throw_dir
    v = get_unit_vector(np.cross(u, (0,0,1)))
    w = tuple(np.cross(u, v))
    pos0, dir0 = get_intersections.hail[0]
    pv0, pw0 = np.inner(pos0, v), np.inner(pos0, w)
    dv0, dw0 = np.inner(dir0, v), np.inner(dir0, w)
    intersects = []
    for pos, dir in get_intersections.hail[1:4]:
        pu, pv, pw = (np.inner(pos, ax) for ax in (u, v, w))
        du, dv, dw = (np.inner(dir, ax) for ax in (u, v, w))
        # pv, pw = np.inner(pos, v), np.inner(pos, w)
        # du, dv, dw = np.inner(dir, v), np.inner(dir, w)
        w_val = (pv - pv0 + pw0 * dv0/dw0 - pw * dv/dw) / (dv0/dw0 - dv/dw)
        t_val = (w_val - pw)/dw
        # v_val = pv + t_val * dv
        # assert math.isclose(v_val, v_val_0 := pv0 + (w_val - pw0) * dv0/dw0)
        intersects.append({
            't': t_val,
            'xyz': tuple(p + t_val * d for p, d in zip(pos, dir)),
            'uvw': (pu + t_val * du, pv + t_val * dv, w_val),
        })
    return intersects
get_intersections.hail = None


print_function
def part_two(input: str) -> int:
    lines = input.split('\n')
    hail = []
    for line in lines:
        nums = list(map(int, re.findall('-?\d+', line)))
        hail.append((tuple(nums[:3]), tuple(nums[3:])))
    get_intersections.hail = hail
    hail.append(hail.pop(2)) # Necessary for example input which contained a parallel hailstone path
    # Visualization
    if visualize := False:
        import matplotlib.pyplot as plt
        axes = plt.figure().add_subplot(111, projection='3d')
        dims = [[1e14, 4e14] for _ in range(3)]
        for (pos, dir) in hail[:4]:
            ts = [None, None]
            for ax in range(3):
                t_1, t_2 = (dims[ax][0] - pos[ax]) / dir[ax], (dims[ax][1] - pos[ax]) / dir[ax]
                min_t, max_t = min(t_1, t_2), max(t_1, t_2)
                ts[0] = min_t if ts[0] == None else max(ts[0], min_t)
                ts[1] = max_t if ts[1] == None else min(ts[1], max_t)
            xyz_plot = [[pos[ax] + ts[0] * dir[ax], pos[ax] + ts[1] * dir[ax]] for ax in range(3)]
            axes.plot(*xyz_plot)
        axes.set_xlabel('X'), axes.set_ylabel('Y'), axes.set_zlabel('Z'), plt.show()
        return
    # Find a rough estimate for the unit vector direction by searching a 20z20z20 grid
    unit_vector = sorted((direction_error_cost(ans), ans) for ans in it.product(range(-10, 11), repeat=3))[0][1]
    # Continue searching in steps of 0.05 down to 1e-10 to improve the unit vector direction
    step = 0.10
    factor = 2.0
    while step > UNIT_VECTOR_FINAL_TOLERANCE:
        new_unit_vector = unit_vector
        min_cost = direction_error_cost(unit_vector)
        for d_unit_vector in it.product(range(-5, 6), repeat=3):
            new_ans = tuple(cur + delta*step for cur, delta in zip(unit_vector, d_unit_vector))
            new_cost = direction_error_cost(new_ans)
            if new_cost < min_cost:
                min_cost = new_cost
                new_unit_vector = new_ans
        unit_vector = get_unit_vector(new_unit_vector)
        step /= factor
    # Calculate the speed between hail point collissions to calculate speed even more accurately
    isec = get_intersections(unit_vector)
    speed = tuple(round((isec[1]['xyz'][ax]-isec[0]['xyz'][ax]) / (isec[1]['t'] - isec[0]['t'])) for ax in range(3))
    # Calculate starting positiong from hail point collission position and time
    isec = get_intersections(speed)
    start = tuple(round(isec[0]['xyz'][ax] - isec[0]['t'] * speed[ax]) for ax in range(3))
    return sum(start)


@print_function
def main(input: str) -> tuple[int, int]:
    return (
        part_one(input), 
        part_two(input),
    )

# aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')

aoc_run( __name__, __file__, main, AOC_ANSWER, 'ex')


