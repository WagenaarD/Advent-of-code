"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2
# 12:22:53

AOC_ANSWER = (49897, 194033958221830)

import sys
sys.path.append(AOC_BASE_PATH := '/'.join(__file__.replace('\\', '/').split('/')[:-3]))
from aoc_tools import print_function, aoc_run

DIRS = {
    'D': ( 1,  0),
    'U': (-1,  0),
    'R': ( 0,  1),
    'L': ( 0, -1),
}
HEX_DICT = {
    '0': 'R',
    '1': 'D',
    '2': 'L',
    '3': 'U',
}

def visualize_part_one(trench: set[tuple[int, int]], seen: set[tuple[int, int]] = set()) -> None:
    
    r_min = min(r for r, c in (trench | seen))
    r_max = max(r for r, c in (trench | seen))
    c_min = min(c for r, c in (trench | seen))
    c_max = max(c for r, c in (trench | seen))
    for r in range(r_min, r_max + 1):
        out = ''
        for c in range(c_min, c_max + 1):
            out += '#' if (r,c) in trench else '~' if (r, c) in seen else '.'
        print(out)


@print_function
def part_one(input: str, vis: bool = True) -> int:
    lines = input.split('\n')
    trench = set()
    pos = (0,0)
    for line in lines:
        dr, dl, color = line.split()
        dr = DIRS[dr]
        for _ in range(int(dl)):
            pos = tuple(p + dp for p, dp in zip(pos, dr))
            trench.add(pos)
    if vis: visualize_part_one(trench)
    
    # Grow from outside
    r_min = min(r for r, c in trench) - 1
    r_max = max(r for r, c in trench) + 1
    c_min = min(c for r, c in trench) - 1
    c_max = max(c for r, c in trench) + 1
    stack = set([(r, c_min) for r in range(r_min, r_max+1)] + \
        [(r, c_max) for r in range(r_min, r_max+1)] + \
        [(r_min, c) for c in range(c_min, c_max+1)] + \
        [(r_max, c) for c in range(c_min, c_max+1)])
    seen = stack.copy()
    while stack:
        r,c = stack.pop()
        for dr, dc in DIRS.values():
            new_pos = (r + dr, c + dc)
            in_bounds = r_min <= new_pos[0] <= r_max and c_min <= new_pos[1] <= c_max
            if in_bounds and new_pos not in seen and new_pos not in trench:
                seen.add(new_pos)
                stack.add(new_pos)
    
    if vis: visualize_part_one(trench, seen)
    ans = 0
    for r in range(r_min, r_max + 1):
        for c in range(c_min, c_max + 1):
            if not (r,c) in seen:
                ans +=1 
    return ans


def get_area(nodes: list[tuple[int, int]]) -> int:
    """
    Polygon area: Signed area: https://www.mathopenref.com/coordpolygonarea.html
    Correction of total_l is necessary as the algorithm calculates the area between a line running 
    in the center of the pixel. However, we want to include the whole pixel:
    - Half the line lengths is added since half of each straight piece is excluded in the signed area
    - One pixel is added to account for outer four corners which have 3/4 excluded.
    - For any additional turn, one corner will have 3/4 excluded and one 1/4 excluded, so no 
    additional correction is needed since they are compensated with 1/2 per length.
    """
    area = 0
    total_l = 0
    for cur, nxt in zip(nodes, nodes[1:]):
        total_l += abs(cur[0] - nxt[0]) + abs(cur[1] - nxt[1])
        area += (cur[0] * nxt[1] - cur[1] * nxt[0]) / 2
    return int(abs(area) + 1 + total_l / 2)


def solve(input: str, part_two = False) -> int:
    lines = input.split('\n')
    pos = (0,0)
    nodes = [pos]
    for line in lines:
        dr, dl, color = line.split()
        dr = DIRS[dr]
        if part_two:
            dr = DIRS[HEX_DICT[color[-2]]]
            dl = int(color[2:-2], 16)
        pos = tuple(p + dp * int(dl) for p, dp in zip(pos, dr))
        nodes.append(pos)
    return get_area(nodes)
    
@print_function
def main(input: str) -> tuple[int, int]:
    return (solve(input, False), solve(input, True))

aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')
# aoc_run(__name__, __file__, main, AOC_ANSWER, 'ex')


