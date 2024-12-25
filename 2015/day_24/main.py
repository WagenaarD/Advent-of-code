"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

AOC_ANSWER = (10439961859, 72050269)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import itertools as it
import math
from collections import defaultdict


@print_function
def solve(input_txt: str, no_groups: int) -> int:
    weights = list(map(int, input_txt.split('\n')))
    target_weight = sum(weights) // no_groups
    # Find the least number of packages with which one third of the weight can be made
    for num_packs in range(len(weights)//no_groups):
        g1_configs = []
        for g1 in it.combinations(weights, num_packs):
            if sum(g1) == target_weight:
                g1_configs.append(g1)
        if g1_configs:
            break
    # Sort group 1 to start with the best scoring one, then iterate over them.
    g1_configs.sort(key = lambda lst: math.prod(lst))
    for g1_config in g1_configs:
        # Check whether the rest of the weights can be equally distributed. If so, return the answer
        remaining_weights = list(set(weights) - set(g1_config))
        for groups in it.product(range(1, no_groups), repeat=len(remaining_weights)):
            group_weights = defaultdict(int)
            for weight, group in zip(remaining_weights, groups):
                group_weights[group] += weight
            if all(weight == target_weight for weight in group_weights.values()):
                return math.prod(g1_config)
        print('!! No valid configuration found')
    # No solution found
    return -1


@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        solve(input_txt, 3), 
        solve(input_txt, 4),
    )

aoc_run( __name__, __file__, main, AOC_ANSWER)
