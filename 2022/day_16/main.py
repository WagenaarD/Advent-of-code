"""
Advent of code challenge 2022
>> python3 main.py < in
Start   - 
Part 1  - 1923 (ex 1651)
Part 2  - (ex 1707)
Cleanup - 
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import re
from functools import cache

AOC_ANSWER = (1923, 2594)

def valve_path(source: str, target: str, valves, d: int = 0) -> list:
    """
    Returns a shortest path between the source and the target. 

    Broad first increase of both source and target until they overlap. Once they overlap, the same 
    algorithm is done between the source and the overlapping node and the node to the target. 
    At some point the source and terget are next to eachother and the direct path is returned
    
    Holy fuck this actually worked. This is apparantly called a Floyd–Warshall algorithm.
    """
    # If next to eachother return result
    if target in valves[source][1]:
        return [source, target]
    # Look from both ends
    source_keys, target_keys = [source], [target]
    source_depth, target_depth = 0, 0
    while True:
        source_depth += 1
        target_depth += 1
        for key in source_keys[:]:
            for valve in valves[key][1]:
                if valve not in source_keys:
                    source_keys.append(valve)
                    if valve in target_keys:
                        return valve_path(source, valve, valves, d+1)[:-1] + valve_path(valve, target, valves, d+1)
        for key in target_keys[:]:
            for valve in valves[key][1]:
                if valve not in target_keys:
                    target_keys.append(valve)
                    if valve in source_keys:
                        return valve_path(source, valve, valves, d+1)[:-1] + valve_path(valve, target, valves, d+1)

C = {}
def valve_distance(source: str, target: str, valves) -> int:
    """Cached wrapper to speed up function calls"""
    if (source, target) not in C:
        C[(source, target)] = len(valve_path(source, target, valves)) - 1
    return C[(source, target)]


def max_release(keys: list, valves, node = 'AA', t = 0, duo = False, t_max = 30):
    if (''.join(keys), node, t, duo, t_max) in max_release.cache:
        return max_release.cache[(''.join(keys), node, t, duo, t_max)]
    flow = [0]
    for key_idx, key in enumerate(keys):
        delta_t = valve_distance(node, key, valves) + 1
        if t + delta_t <= t_max:
            flow.append(max_release(
                keys = keys[:key_idx] + keys[key_idx + 1:],
                valves = valves,
                node = key,
                t = t + delta_t,
                duo = duo,
                t_max = t_max,
                ) + valves[key][0] * (t_max - (t + delta_t))
            )
    if duo:
        flow.append(max_release(
            keys = keys,
            valves = valves,
            node = 'AA',
            t = 0,
            duo = False, 
            t_max = t_max,
            )
        )
    max_release.cache[(''.join(keys), node, t, duo, t_max)] = max(flow)
    return max(flow)
max_release.cache = {}


@print_function
def solve_part_1(non_zero_valve_keys, valves):
    return max_release(non_zero_valve_keys, valves, t_max = 30, duo = False)

@print_function
def solve_part_2(non_zero_valve_keys, valves):
    return max_release(non_zero_valve_keys, valves, t_max = 26, duo = True)


@print_function
def main(input_txt: str) -> tuple[int, int]:    
    lines = input_txt.split('\n')

    # Process input
    valves = {}
    for line in lines:
        valves[line[6:8]] = (
            int(re.findall('[0-9]+', line)[0]),
            line.replace(',', '').split()[9:],
        )
    non_zero_valve_keys = [key for key, value in valves.items() if value[0] > 0]
    
    return (
        solve_part_1(non_zero_valve_keys, valves),
        solve_part_2(non_zero_valve_keys, valves),
    )

aoc_run(__name__, __file__, main, AOC_ANSWER)
