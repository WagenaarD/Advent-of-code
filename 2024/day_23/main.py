"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""
# 12:39:44
# 12:50:34
# 13:56:22

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import itertools as it
from collections import defaultdict
from functools import cache, reduce

AOC_ANSWER = (1400, 'am,bc,cz,dc,gy,hk,li,qf,th,tj,wf,xk,xo')


@print_function
def part_one(input_txt: str) -> int:
    """
    Find the number combinations of three PCs that are directly connected and had at least one PC 
    starting with the letter 't'
    """
    lines = input_txt.split('\n')
    pairs = defaultdict(list)
    for line in lines:
        p1, p2 = line.split('-')
        pairs[p1].append(p2)
        pairs[p2].append(p1)
    sets_of_three = set()
    for pc1 in pairs:
        for pc2, pc3 in it.combinations(pairs[pc1], r=2):
            if pc3 in pairs[pc2]:
                sets_of_three.add(tuple(sorted((pc1, pc2, pc3))))
    return sum(1 for pcs in sets_of_three if any(pc.startswith('t') for pc in pcs))


@print_function
def part_two(input_txt: str) -> int:
    """
    Find the largest set of PCs which are all connected to every other PC in the set
    The calculates the largest theoretically possible set based on the maximum number of connections
    to a single PC (max_n). Then, we iterate over combinations of max_n length that are all 
    connected to one PC. If none are found, we reduce max_n by one and try again. The first solution
    we find is always the largest one.

    This is fast because (1) there is not much variation in the number of connecting PCs (each PC is
    connceted to 13 other PCs, making the maximum connected set 14), and (2) the largest possible 
    set is 13 PCs, making the number of combinations small (14 per PC).
    """
    lines = input_txt.split('\n')
    pairs = defaultdict(set)
    for line in lines:
        p1, p2 = line.split('-')
        pairs[p1].update({p1, p2})
        pairs[p2].update({p1, p2})
    max_n = max(map(len, pairs.values())) + 1
    for max_n in range(max_n, 1, -1):
        print(f'{max_n}')
        for superset in pairs.values():
            for subset in it.combinations(superset, max_n-1):
                connections = reduce(set.intersection, [pairs[pc] for pc in subset])
                if all(pc in connections for pc in subset):
                    return ','.join(sorted(set(subset)))
                

@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        part_one(input_txt), 
        part_two(input_txt)
    )
aoc_run(__name__, __file__, main, AOC_ANSWER)


