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

class NetworkPairs:
    def __init__(self, pairs: dict[set[str]]):
        self.pairs = pairs
    
    @cache
    def get_biggest_inteconnected(self, pcs: tuple[str]) -> tuple[str]:
        """Returns the largest group of PCs which are all connected to eachother directly."""
        answers = [pcs]
        for next_pc in self.get_pair_intersection(pcs):
            answers.append(self.get_biggest_inteconnected(tuple(sorted(pcs + (next_pc,)))))
        return sorted(answers, key=len)[-1]
    
    @cache
    def get_pair_intersection(self, pcs: tuple[str]) -> set[str]:
        """Returns the set of PCs which are connected to all PCs in the argument."""
        return reduce(set.intersection, [self.pairs[pc] for pc in pcs])


@print_function
def part_two(input_txt: str) -> int:
    """Find the largest set of PCs which are all connected to every other PC in the set"""
    lines = input_txt.split('\n')
    pairs = defaultdict(set)
    for line in lines:
        p1, p2 = line.split('-')
        pairs[p1].add(p2)
        pairs[p2].add(p1)
    ans = []
    np = NetworkPairs(pairs)
    for pc in list(pairs):
        ans.append(np.get_biggest_inteconnected((pc,)))
    return ','.join(sorted(sorted(ans, key=len)[-1]))

@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        part_one(input_txt), 
        part_two(input_txt)
    )
aoc_run(__name__, __file__, main, AOC_ANSWER)


