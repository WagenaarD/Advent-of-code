"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (None, None)

import sys
sys.path.append(AOC_BASE_PATH := '/'.join(__file__.replace('\\', '/').split('/')[:-3]))
from aoc_tools import print_function
import itertools as it
from dataclasses import dataclass, field
from collections import defaultdict
import re
import numpy as np
from pprint import pprint
from functools import cache
import math

"""
broadcaster
%: Flip-flop
&: Conjunction
"""

def press_button(modules: dict, log = False) -> tuple[int, int]:    
    stack = [('broadcaster', False, 'button')]
    total_pulses = [0, 0]
    while stack:
        pls_target, pls_strength, pls_source = stack.pop(0)
        if log: print(f'{pls_source} -{"high" if pls_strength else "low"}-> {pls_target}')
        total_pulses[pls_strength] += 1
        if not pls_target in modules:
            continue
        mod_type, mod_targets, state, inputs = modules[pls_target]
        if mod_type == 'b':
            # broadcaster
            for mod_target in mod_targets:
                stack.append((mod_target, pls_strength, pls_target))
        elif mod_type == '%': 
            # Flip-flop
            # If a flip-flop module receives a high pulse, it is ignored and nothing happens. 
            # However, if a flip-flop module receives a low pulse, it flips between on and off. 
            if not pls_strength:
                state = not state
                modules[pls_target] = (mod_type, mod_targets, state, inputs)
                # If it was off, it turns on and sends a high pulse. If it was on, it turns off and 
                # sends a low pulse.
                new_pls_strength = state
                for mod_target in mod_targets:
                    stack.append((mod_target, new_pls_strength, pls_target))
        elif mod_type == '&':
            # Conjunction
            # Conjunction modules (prefix &) remember the type of the most recent pulse received 
            # from each of their connected input modules; they initially default to remembering a 
            # low pulse for each input. 
            # When a pulse is received, the conjunction module first updates its memory for that input. 
            inputs[pls_source] = pls_strength
            # Then, if it remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends a high pulse.
            new_pls_strength = not all(inputs.values())
            for mod_target in mod_targets:
                stack.append((mod_target, new_pls_strength, pls_target))
    return total_pulses


@print_function
def part_one(input: str) -> int:
    lines = input.split('\n')
    modules = {}
    for line in lines:
        left, right = line.split(' -> ')
        if left == 'broadcaster':
            modules['broadcaster'] = ['b', right.split(', '), False, {}]
        else:
            # Flip-flop or conjunction
            # [0] mod_type
            # [1] mod_targets
            # [2] state (Used by flip-flop modules)
            # [3] inputs (Used by conjunction modules)
            modules[left[1:]] = [left[0], right.split(', '), False, {}]
    # Record all inputs for conjunction modules
    for mod_name, (mod_type, targets, state, inputs) in modules.items():
        for pls_target in targets:
            if pls_target in modules:
                modules[pls_target][3][mod_name] = False
    # pprint(modules)
    # Process the button press
    low_tot, hi_tot = 0, 0
    for idx in range(1_000):
        low, hi = press_button(modules)
        low_tot += low
        hi_tot += hi
    return low_tot * hi_tot

    








@print_function
def part_two(input: str) -> int:
    lines = input.split('\n')
# @print_function
# def main(input: str) -> tuple[int, int]:
#     return (part_one(input), part_two(input))
if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    input = sys.stdin.read().strip()
    print(part_one(input) == AOC_ANSWER[0])
    print(part_two(input) == AOC_ANSWER[1])
    # print('  ->', main(input) == (AOC_ANSWER[0], AOC_ANSWER[1]))


