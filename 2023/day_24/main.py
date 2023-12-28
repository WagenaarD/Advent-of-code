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
from dataclasses import dataclass, field
from collections import defaultdict, deque, Counter
import re
import numpy as np
from pprint import pprint
from functools import cache
import math
import operator
import z3
from fractions import Fraction
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
            print(f'\nHailstone A: {pos1} @ {vel1}')
            print(f'Hailstone B: {pos2} @ {vel2}')
            # try:
            b1 = vel1[1] / vel1[0]
            a1 = pos1[1] - pos1[0] * b1
            b2 = vel2[1] / vel2[0]
            a2 = pos2[1] - pos2[0] * b2
            if b1 == b2:
                print("Hailstones' paths are parallel; they never intersect.")
                continue
            x = (a1 - a2) / (b2 - b1)
            y = a1 + b1 * x
            t1 = (x-pos1[0])/vel1[0]
            t2 = (x-pos2[0])/vel2[0]
            in_test = lower <= x <= upper and lower <= y <= upper
            # if lower <= x <= upper and lower <= y <= upper:
            #     ans +=1 
            if t1 < 0 and t2 < 0:
                print("Hailstones' paths crossed in the past for both hailstones.")
            if t1 < 0:
                print("Hailstones' paths crossed in the past for hailstone A.")
            elif t2 < 0:
                print("Hailstones' paths crossed in the past for hailstone B.")
            elif in_test:
                print("Hailstones' paths will cross inside the test area (at x={}, y={}).".format(x, y))
                ans += 1
            else:
                print("Hailstones' paths will cross outside the test area.")

            # except ZeroDivisionError:
            #     pass
    print(ans)
    return ans

            
@print_function
def part_two_z3(input: str) -> int:
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
    print([model[arg].as_long() for arg in (Xso, Yso, Zso, Vxs, Vys, Vzs)])
    assert False
    return sum(model[arg].as_long() for arg in (Xso, Yso, Zso))

print_function
def part_two(input: str) -> int:
    lines = input.split('\n')
    hail = []
    for line in lines:
        nums = list(map(int, re.findall('-?\d+', line)))
        hail.append((tuple(nums[:3]), tuple(nums[3:])))
    vector = (-3, 1, 2) if (is_ex := (len(lines) < 10)) else (-299, -98, 79)

    # Visualization
    if visualize := False:
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

    # # Visualize along axis of first hail
    # u = get_unit_vector(hail[0][1])
    # v = outer_product(u, (0,0,1))
    # w = outer_product(u, v)
    # def rotation_around_axis(axis, angle):
    #     sin, cos = math.sin(angle * math.pi/180), math.cos(angle * math.pi/180)
    #     x,y,z = axis
    #     return np.array([
    #         [cos + x**2*(1-cos),   x*y*(1-cos) - z*sin,   x*z*(1-cos) + y*sin],
    #         [y*x*(1-cos) + z*sin,   cos + y**2*(1-cos),    y*z*(1-cos)-x*sin  ],
    #         [z*x*(1-cos) - y*sin,   z*y*(1-cos) + x*sin,   cos + z**2*(1-cos)  ],
    #     ])
    # R = np.inner(rotation_around_axis(u, -30), rotation_around_axis(v, 30))
    # u, v, w = (np.inner(ax, R) for ax in (u, v, w))
    # axes = plt.figure().add_subplot()
    # dims = [[1e14, 4e14] for _ in range(3)]
    # for (pos, dir) in hail[:4]:
    #     ts = [None, None]
    #     for ax in range(3):
    #         t_1, t_2 = (dims[ax][0] - pos[ax]) / dir[ax], (dims[ax][1] - pos[ax]) / dir[ax]
    #         min_t, max_t = min(t_1, t_2), max(t_1, t_2)
    #         ts[0] = min_t if ts[0] == None else max(ts[0], min_t)
    #         ts[1] = max_t if ts[1] == None else min(ts[1], max_t)
    #     pos = tuple(np.inner(ax, pos) for ax in (u,v,w))
    #     dir = tuple(np.inner(ax, dir) for ax in (u,v,w))
    #     # uwv_plot = [[pos[ax] + ts[0] * dir[ax], pos[ax] + ts[1] * dir[ax]] for ax in range(3)]
    #     # axes.plot(*uwv_plot)
    #     uv_plot = [[pos[ax] + ts[0] * dir[ax], pos[ax] + ts[1] * dir[ax]] for ax in (0,1)]
    #     axes.plot(*uv_plot)
    # axes.set_xlabel('U'), axes.set_ylabel('V'), plt.show()

    # Solve Numerically
    @cache
    def cost(projection_dir: tuple) -> float:
        projection_dir = get_unit_vector(projection_dir)
        if abs(projection_dir[2]) > 0.999: return 1e30
        u = projection_dir
        v = get_unit_vector(outer_product(u, (0,0,1)))
        w = outer_product(u, v)
        pos0, dir0 = hail[0]
        pv0, pw0 = np.inner(pos0, v), np.inner(pos0, w)
        dv0, dw0 = np.inner(dir0, v), np.inner(dir0, w)
        isec = []
        for pos, dir in hail[1:4]:
            pv, pw = np.inner(pos, v), np.inner(pos, w)
            dv, dw = np.inner(dir, v), np.inner(dir, w)
            w_val = (pv - pv0 + pw0 * dv0/dw0 - pw * dv/dw) / (dv0/dw0 - dv/dw)
            v_val = pv + (w_val - pw) * dv/dw
            # assert math.isclose(v_val, v_val_0 := pv0 + (w_val - pw0) * dv0/dw0)
            isec.append((v_val, w_val))
        return sum([(isec[x][ax] - isec[y][ax]) ** 2 for ax in range(2) for x, y in ((0,1), (1, 2), (2, 0))])

    def yaw_and_pitch_vector(y, p):
        base = (0,0,1)
        yaw = np.array([
            [math.cos(y), -math.sin(y), 0],
            [math.sin(y), math.cos(y), 0],
            [0, 0, 1]
        ])
        pitch = np.array([
            [math.cos(p), 0, math.sin(p)],
            [0, 1, 0],
            [-math.sin(p), 0, math.cos(p)],
        ])
        return np.inner(np.inner(base, pitch), yaw)

    @cache
    def cost_yp(y, p):
        # if (y, p) == (0,0): return 1e30
        return cost(yaw_and_pitch_vector(y * math.pi/180, p * math.pi/180))

    # y, p = 1,1 
    # STEP = 10
    # FACTOR = 1.2
    # step = STEP
    # min_cost = cost_yp(y, p)
    # while step > 1e-2:
    #     print(y, p, cost_yp(y, p), step)
    #     for yi in range(0, int(360 // step)):
    #         yi *= step
    #         if cost_yp(yi, p) < min_cost:
    #             y, min_cost = yi, cost_yp(yi, p)
    #     for pi in range(0, int(360 // step)):
    #         pi *= step
    #         if cost_yp(y, pi) < min_cost:
    #             p, min_cost = pi, cost_yp(y, pi)
    #     step /= FACTOR
    
    # Find a rough estimate for the unit vector direction
    STEP = 10
    ans = (1,1,1)
    min_cost = cost(get_unit_vector(ans))
    for dx, dy, dz in print_loop(it.product(range(-10, 11), repeat=3), 2e2**3):
        if (dx, dy, dz) == (0,0,0):
            continue
        uv = get_unit_vector((dx,dy,dz))
        c = cost(uv)
        if c < min_cost:
            ans = (dx,dy,dz)
            min_cost = c
    # Make a finer estimate accurate to 0.01
    step = 0.05
    factor = 1.5
    while step > 1e-10:
        for d_ans in it.product(range(-5, 6), repeat=3):
            new_ans = tuple(an + dan*step for an, dan in zip(ans, d_ans))
            new_cost = cost(new_ans)
            if new_cost < min_cost:
                min_cost = new_cost
                new_best_ans = new_ans
        ans = get_unit_vector(new_best_ans)
        step /= factor
        print(step, tuple(an-v for an,v in zip(ans, get_unit_vector((vector)))))
    print(ans, get_unit_vector(vector), cost(ans), cost(vector))
    
    # Find time hail points reach the point along the unit vector
    u = get_unit_vector(ans)
    v = get_unit_vector(outer_product(u, (0,0,1)))
    w = outer_product(u, v)
    pos0, dir0 = hail[0]
    pu0, pv0, pw0 = np.inner(pos0, u), np.inner(pos0, v), np.inner(pos0, w)
    vu0, dv0, dw0 = np.inner(dir0, u), np.inner(dir0, v), np.inner(dir0, w)
    isec = []
    for pos, dir in hail[1:3]:
        x, y, z = pos
        dx, dy, dz = dir
        pu, pv, pw = np.inner(pos, u), np.inner(pos, v), np.inner(pos, w)
        du, dv, dw = np.inner(dir, u), np.inner(dir, v), np.inner(dir, w)
        w_val = (pv - pv0 + pw0 * dv0/dw0 - pw * dv/dw) / (dv0/dw0 - dv/dw)
        t = (w_val-pw)/dw
        # v_val = pv + t * dv
        # u_val = pu + t * du
        # assert math.isclose(v_val, v_val_0 := pv0 + (w_val - pw0) * dv0/dw0)
        isec.append((t, (x + dx * t, y + dy * t, z + dz * t)))
    dir_ans = tuple(round((isec[1][1][ax]-isec[0][1][ax]) / (isec[1][0] - isec[0][0])) for ax in range(3))
    

    # Now we need to recalculate the intersection to find the position answer
    u = get_unit_vector(dir_ans)
    v = get_unit_vector(outer_product(u, (0,0,1)))
    w = outer_product(u, v)
    pos0, dir0 = hail[0]
    pu0, pv0, pw0 = np.inner(pos0, u), np.inner(pos0, v), np.inner(pos0, w)
    vu0, dv0, dw0 = np.inner(dir0, u), np.inner(dir0, v), np.inner(dir0, w)
    isec = []
    for pos, dir in hail[1:2]:
        x, y, z = pos
        dx, dy, dz = dir
        pu, pv, pw = np.inner(pos, u), np.inner(pos, v), np.inner(pos, w)
        du, dv, dw = np.inner(dir, u), np.inner(dir, v), np.inner(dir, w)
        w_val = (pv - pv0 + pw0 * dv0/dw0 - pw * dv/dw) / (dv0/dw0 - dv/dw)
        t = (w_val-pw)/dw
        # v_val = pv + t * dv
        # u_val = pu + t * du
        # assert math.isclose(v_val, v_val_0 := pv0 + (w_val - pw0) * dv0/dw0)
        isec.append((t, (x + dx * t, y + dy * t, z + dz * t)))    
    t, pos = isec[0]
    pos_ans = tuple(round(pos[ax] - t * dir_ans[ax]) for ax in range(3))
    print(pos_ans)
    print(sum(pos_ans))
    assert False



    # 
    # act = True
    # while act:
    #     min_cost = cost_yp(y, p)
    #     act = False
    #     for yi in range(0, 360, STEP):
    #         if cost_yp(yi, p) < min_cost:
    #             min_cost = cost_yp(yi, p)
    #             y = yi
    #             act = True
    #     for pi in range(0, 360, STEP):
    #         if cost_yp(y, pi) < min_cost:
    #             min_cost = cost_yp(y, pi)
    #             p = pi
    #             act = True
    # STEP /= FACTOR
    # while True:
    #     print(STEP, y, p, cost_yp(y, p))
    #     while cost_yp(y+STEP, p) < cost_yp(y, p):
    #         y += STEP
    #     while cost_yp(y, p+STEP) < cost_yp(y, p):
    #         p += STEP
    #     while cost_yp(y-STEP, p) < cost_yp(y, p):
    #         y -= STEP
    #     while cost_yp(y, p-STEP) < cost_yp(y, p):
    #         p -= STEP
    #     STEP /= FACTOR
        
    #     if STEP < 1e-10:
    #         break
    # uv = yaw_and_pitch_vector(y, p)
    # correct_uv = get_unit_vector(vector)
    # print(uv, correct_uv, cost(uv), cost(correct_uv))
    
    



        



    


        


    # # Find unit vectors
    # for idx, (hpos, hdir) in enumerate(hail):
    #     for other_pos, other_dir in hail[idx+1:]:
    #         if paths_parrallel(hdir, other_dir):
    #             print('!!! parallel', (hpos, hdir), (other_pos, other_dir))
    #         elif hails_intersect_3d((hpos, hdir), (other_pos, other_dir)):
    #             print('!!! intersecting!', (hpos, hdir), (other_pos, other_dir))
    

    # unit_vectors = []
    # for hpos, hdir in hail:
    #     unit_vector = get_unit_vector(hdir)
    #     # inverted_unit_vector = (-unit_vector[0], -unit_vector[1], -unit_vector[2], unit_vector[3])
    #     # inverted_unit_vector = tuple(-v for v in unit_vector)
    #     # if unit_vector in unit_vectors:
    #     #     print('!!!')
    #     # elif inverted_unit_vector in unit_vectors:
    #     #     print('!!! inverted')
    #     # elif any(all(math.isclose(unit_vector[idx], other[idx], abs_tol = 1E-10) for idx in range(3)) for other in unit_vectors):
    #     #     print('!!! close')
    #     unit_vectors.append(unit_vector)
    #     unit_vectors.append(inverted_unit_vector)
    # assert False
    # Find two vectors with at least one axis the same
    
    # for idx, (hpos, hdir) in enumerate(hail):
    #     if any(hdir[0] == other[1][0] for other in hail[idx+1:]):
    #         dir_1 = hdir
    #          for other in hail[idx+1:] if hdir[0] == other[1][0]]
    #         break
        
    

    # hpos, hdir1 = hail[0]
    # hpos, hdir2 = hail[1]
    # hpos, hdir3 = hail[3]
    # hpos, hdir4 = hail[4]

    # op1 = outer_product(get_unit_vector(hdir1), get_unit_vector(hdir2))
    # op2 = outer_product(get_unit_vector(hdir2), get_unit_vector(hdir3))
    # op3 = outer_product(get_unit_vector(hdir3), get_unit_vector(hdir4))
    
    # dir1 = outer_product(op1, op2)
    # dir2 = outer_product(op2, op3)
    # dir3 = outer_product(op1, op3)
    # assert False




    
    
    # max_idx = 0
    # while True:
    #     max_idx += 1
    #     print(max_idx)
    #     for vector_values in it.product(range(-max_idx, max_idx+1), repeat = 3):
    #         if max(map(abs, vector_values)) < max_idx:
    #             continue
    #         # print(vector_values)
    #         if vector_valid(vector_values, hail) < TOLERANCE:
    #             break
    #     else:
    #         # assert vector_values != vector
    #         # assert vector_values[0] != -2 and max_idx == 3
    #         # assert max_idx < 4
    #         continue
    #     break
    # print(vector_values) 
    # # Two options exist, positive and negative
    # for sign in (1, -1):
    #     # y = y0 + (x - x0) * dy/dx
    #     # ys = y0
    #     hpos, hdir = hail[0]
    #     x0, y0, z0 = hpos
    #     dx0, dy0, dz0 = hdir
    #     # y0 + (x - x0) * dy0/dx0 = ys + (x - xs) * dys/dxs
    #     # y0 - ys = x * dys/dxs - xs * dys/dxs - x * dy0/dx0 + x0 * dy0/dx0
    #     # y0 - ys + xs * dys/dxs - x0 * dy0/dx0 = x * (dys/dxs - dy0/dx0)
    #     # x = (y0 - ys + xs * dys/dxs - x0 * dy0/dx0) / (dys/dxs - dy0/dx0)


    
    
    
    
    # assert False


    
    # print(vector_valid(vector, hail))
    
    



    



def get_unit_vector(vector: tuple[float, float, float]) -> tuple[float, float, float]:
    sqrt_sq_sum = math.sqrt(sum(vs**2 for vs in vector))
    return tuple(v/sqrt_sq_sum for v in vector)
    # # gcd = int(math.gcd(*vector, sq_sum))
    # return tuple(Fraction(v, gcd) for v in vector) + (sq_sum/gcd,)

def paths_parrallel(vector, other) -> bool:
    uv_1 = get_unit_vector(vector)
    uv_2 = get_unit_vector(other)
    inv_uv_2 = tuple(-v for v in uv_2)
    return uv_1 == uv_2 or uv_1 == inv_uv_2

def hails_intersect_3d(hail, other) -> bool:
    pos_0, dir_0 = hail
    pos_1, dir_1 = other
    # y = y
    # y0 + (x-x0) / (vy0/vx0) = y1 + (x-x1) / (vy1/vx1)
    # y0 - y1 = x / (vy1/vx1) - x1 / (vy1/vx1) - x / (vy0/vx0) + x0 / (vy0/vx0)
    # y0 - y1 + x1 / (vy1/vx1) - x0 / (vy0/vx0) = x *(1 / (vy1/vx1) - 1 / (vy0/vx0))
    # x = y0 - y1 + x1 / (vy1/vx1) - x0 / (vy0/vx0) / (1 / (vy1/vx1) - 1 / (vy0/vx0))
    x0, y0, z0 = pos_0
    vx0, vy0, vz0 = dir_0
    x1, y1, z1 = pos_1
    vx1, vy1, vz1 = dir_1
    if vy1/vx1 == vy0/vx0:
        return False 
    x_inter = (y0 - y1 + x1 / (vy1/vx1) - x0 / (vy0/vx0)) / (1 / (vy1/vx1) - 1 / (vy0/vx0))
    y_inter = y0 + (x_inter-x0) / (vy0/vx0)
    assert math.isclose(y_inter, y1 + (x_inter-x1) / (vy1/vx1), abs_tol=1E-10)
    z_inter_0 = z0 + (x_inter-x0) / (vz0/vx0)
    z_inter_1 = z1 + (x_inter-x0) / (vz1/vx0)
    return math.isclose(z_inter_0, z_inter_1, abs_tol=1E-10)









def outer_product(a: tuple, b: tuple) -> tuple:
    return (a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0])

def inner_product(a: tuple, b: tuple) -> tuple:
    return tuple(a[ax]*b[ax] for ax in range(3))


def vector_valid(vector: tuple[int,int,int], hail: list[tuple[int,int,int], tuple[int,int,int]]) -> bool:
    if sum(map(abs, vector)) == 0:
        return 1_000_000
    unit_vector = tuple(v/math.sqrt(sum(vs**2 for vs in vector)) for v in vector)
    z_ax = np.array(unit_vector)
    rot = np.array([1, 0, 0]) if abs(z_ax[0]) < 0.9 else np.array([0, 1, 0])
    
    # x_ax = np.array([rot[1]*z_ax[2] - rot[2]*z
    # x_ax = np.outer(z_ax, rot)[:,0]
    # y_ax = np.outer(z_ax, x_ax)[:,0]
    x_ax = outer_product(z_ax, rot)
    y_ax = outer_product(z_ax, x_ax)
    assert np.inner(z_ax, x_ax) < TOLERANCE
    assert np.inner(z_ax, y_ax) < TOLERANCE
    assert np.inner(x_ax, y_ax) < TOLERANCE
    # Find two hails that are not parallel and are not vertical
    data = []
    for hpos, hdir in hail:
        x0 = np.inner(x_ax, np.array(hpos))
        y0 = np.inner(y_ax, np.array(hpos))
        dx0 = np.inner(x_ax, np.array(hdir))
        dy0 = np.inner(y_ax, np.array(hdir))
        if dx0 == 0:
            continue
        if len(data) == 1 and dy0/dx0 == data[0][3]/data[0][2]:
            continue
        data.append((x0, y0, dx0, dy0))
        if len(data) == 2:
            break
    else:
        assert False
    # Find the intersection        
    # # Then second h
    # hpos, hdir = hail[1]
    # x1 = np.inner(x_ax, np.array(hpos))
    # y1 = np.inner(y_ax, np.array(hpos))
    # dx1 = np.inner(x_ax, np.array(hdir))
    # dy1 = np.inner(y_ax, np.array(hdir))
    # Find intersection
    # y'(x') = y + (x' - x) * dy/dx
    # y0=y1
    # y0 + (x - x0) * dy0/dx0 = y1 + (x - x1) * dy1/dx1
    # y0 - y1 = x * dy1/dx1 - x1 * dy1/dx1 - x * dyo/dx0 + x0 * dy0/dx0
    # y0 - y1 + x1 * dy1/dx1 - x0 * dy0/dx0 = x * (dy1/dx1 - dy0/dx0)
    # x = (y0 - y1 + x1 * dy1/dx1 - x0 * dy0/dx0) / (dy1/dx1 - dy0/dx0)
    # if dx0 == 0:
    #     return False
    # if dx1 == 0:
    #     return False
    # if (dy1/dx1 - dy0/dx0) == 0:
    #     return False
    x0, y0, dx0, dy0 = data[0]
    x1, y1, dx1, dy1 = data[1]
    x = (y0 - y1 + x1 * dy1/dx1 - x0 * dy0/dx0) / (dy1/dx1 - dy0/dx0)
    y = y0 + (x - x0) * dy0/dx0
    inter = (x, y)
    max_error = 1_000_000
    # hpos, hdir = hail[0]
    for hpos, hdir in hail:
        x0 = np.inner(x_ax, np.array(hpos))
        y0 = np.inner(y_ax, np.array(hpos))
        dx0 = np.dot(x_ax, np.array(hdir))
        dy0 = np.inner(y_ax, np.array(hdir))
        if dx0 == 0:
            # print(f'{(x0, y0)=} {inter=}', x0-inter[0])
            max_error = max(max_error, abs(x0 - inter[0]))
        else:
            y = y0 + (x - x0) * dy0/dx0
            # print(f'{(x, y)=} {inter=}', y-inter[1])
            max_error = max(max_error, abs(x0 - inter[0]))
    return max_error




@print_function
def main(input: str) -> tuple[int, int]:
    return (
        # part_one(input), 
        part_two(input),
    )
aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')
# aoc_run(__name__, __file__, main, AOC_ANSWER, 'ex')


