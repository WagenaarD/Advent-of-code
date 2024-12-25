"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (613870, None)

import sys
sys.path.append(AOC_BASE_PATH := '/'.join(__file__.replace('\\', '/').split('/')[:-3]))
from aoc_tools import print_function, aoc_run, print_loop
import itertools as it
from collections import defaultdict
from pprint import pprint
from datetime import datetime
import math


def get_uncuttable_edges(connect, max_bfs_idx = 5_000):
    uncuttable_edges = []
    for source in print_loop(list(connect)):
        for target in connect[source]:
            if tuple(sorted([source, target])) in uncuttable_edges:
                continue
            solutions = []
            solution_edges = []
            stack = [(source, [], [])]
            bfs_idx = 0
            while stack:
                bfs_idx += 1
                current, seen_edges, seen_vertices = stack.pop(0) 
                if any(edge in solution_edges for edge in seen_edges):
                    continue
                if bfs_idx >= max_bfs_idx:
                    break
                for link in connect[current]:
                    edge = tuple(sorted([current, link]))
                    if edge in solution_edges:
                        continue
                    if link in seen_vertices:
                        continue
                    if edge in seen_edges:
                        continue
                    if link == target:
                        for e in seen_edges + [edge]:
                            solution_edges.append(e)
                        solutions.append((current, seen_edges + [edge]))
                        if len(solutions) > 3:
                            stack = []
                            uncuttable_edges.append(tuple(sorted([source, target])))
                            break
                        continue
                    stack.append((link, seen_edges + [edge], seen_vertices + [link]))
    return uncuttable_edges
            

@print_function
def main(input: str) -> tuple[int, None]:
    # Parse the input
    lines = input.split('\n')
    connect = defaultdict(set)
    for line in lines:
        key, vals = line.split(': ')
        vals = vals.split(' ')
        for val in vals:
            connect[val].add(key)
            connect[key].add(val)
    device_names = list(connect)
    # Get a list of all connections
    all_edges = set()
    for dev_1, connected_to_dev1 in connect.items():
        for dev_2 in connected_to_dev1:
            all_edges.add(tuple(sorted([dev_1, dev_2])))
    uncuttable_edges = get_uncuttable_edges(connect)
    cuttable_edges = [edge for edge in all_edges if edge not in uncuttable_edges]
    print(f'Reduced cuttable edges from {len(all_edges)} to {len(cuttable_edges)}')
    # Sever three random edges and test if we end up with two groups
    start = device_names[0]
    max_idx = math.prod([len(cuttable_edges) - idx for idx in range(3)])
    for severed in print_loop(it.combinations(cuttable_edges, 3), max_idx):
        seen = {start}
        stack = [start]
        while stack:
            current = stack.pop()
            for elem in connect[current]:
                if (current, elem) in severed or (elem, current) in severed:
                    continue
                if elem in seen:
                    continue
                stack.append(elem)
                seen.add(elem)
        assert len(seen) <= len(device_names)
        if len(seen) < len(device_names):
            ans = len(seen) * (len(device_names) - len(seen))
            break
    return ans, None        

aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')
# aoc_run(__name__, __file__, main, AOC_ANSWER, 'ex')
