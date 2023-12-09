"""
Advent of code challenge 2022
>> python3 main.py < in
Start   - 
Part 1  - 4737443 (ex 26)
Part 2  - 11482462818989 (ex 56000011) (18s)
Cleanup - 
"""


import sys
import re
sys.path.insert(0, '/'.join(__file__.replace('\\', '/').split('/')[:-2]))
from _utils.print_function import print_function

def all_numbers(s): return [int(d) for d in re.findall("(-?\d+)", s)]
def md(p, q): return abs(p[0]-q[0])+abs(p[1]-q[1])

def can_be_beacon(x: int, y: int, sensors: list) -> bool:
    for (sx, sy, sd) in sensors:
        coord_distance = abs(sx - x) + abs(sy - y)
        if coord_distance <= sd:
            return False
    return True

@print_function(run_time = True)
def solve():
    input_data = sys.stdin.read().strip()
    data = [all_numbers(line) for line in input_data.split("\n")]
    radius = {(a,b):md((a,b),(c,d)) for (a,b,c,d) in data}
    scanners = radius.keys()

    lines = input_data.split('\n')
    int_lines = [list(map(int, re.findall('-?[0-9]+', line))) for line in lines]
    sensors = [(s[0], s[1], abs(s[0] - s[2]) + abs(s[1] - s[3])) for s in int_lines]

    pos_a_coeffs, neg_a_coeffs, pos_b_coeffs, neg_b_coeffs = [], [], [], []
    for ((x,y), r) in radius.items():
        pos_a_coeffs.append(y-x+r+1)
        neg_a_coeffs.append(y-x-r-1)
        pos_b_coeffs.append(x+y+r+1)
        neg_b_coeffs.append(x+y-r-1)
    a_coeffs = {a for a in pos_a_coeffs if a in neg_a_coeffs}
    b_coeffs = {b for b in pos_b_coeffs if b in neg_b_coeffs}
    # acoeffs = {a for a in acoeffs if acoeffs.count(a) >= 2}
    # bcoeffs = {b for b in bcoeffs if bcoeffs.count(b) >= 2}
    bound = 4_000_000 if input_data.count('\n') != 13 else 20
    for a in a_coeffs:
        for x in range(0, bound + 1):
            y = a + x # a = y - x
            if 0 <= x <= bound and 0 <= y <= bound:
                if can_be_beacon(x, y, sensors):
                    print(x, y, 4_000_000*x+y)
    for b in b_coeffs:
        for x in range(0, bound + 1):
            y = b - x # b = y + x
            if 0 <= x <= bound and 0 <= y <= bound:
                if can_be_beacon(x, y, sensors):
                    print(x, y, 4_000_000*x+y)
    

    # for a in acoeffs:

    #     for b in bcoeffs:
    #         p = ((b-a)//2, (a+b)//2)
    #         if all(0<c<bound for c in p):
    #             if all(md(p,t)>radius[t] for t in scanners):
    #                 print(4_000_000*p[0]+p[1])

solve()
