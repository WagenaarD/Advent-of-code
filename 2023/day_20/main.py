"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (861743850, 247023644760071)

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
import time

"""
broadcaster
%: Flip-flop
&: Conjunction
"""

def press_button(modules: dict, rx_source: str, log: bool = False) -> list[int, int, list[str]]:    
    stack = [('broadcaster', False, 'button')]
    output = [0, 0, []]
    while stack:
        pls_target, pls_strength, pls_source = stack.pop(0)
        if log: print(f'{pls_source} -{"high" if pls_strength else "low"}-> {pls_target}')
        output[pls_strength] += 1
        if pls_target == rx_source:
            if pls_strength: 
                output[2].append(pls_source)
        if not pls_target in modules:
            continue
        mod_type, mod_targets, state, inputs = modules[pls_target]
        if mod_type == 'b':
            # broadcaster
            for mod_target in mod_targets:
                stack.append((mod_target, pls_strength, pls_target))
        elif mod_type == '%': 
            # Flip-flop % 
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
            # Conjunction &
            # Conjunction modules (prefix &) remember the type of the most recent pulse received 
            # from each of their connected input modules; they initially default to remembering a 
            # low pulse for each input. 
            # When a pulse is received, the conjunction module first updates its memory for that input. 
            inputs[pls_source] = pls_strength
            # Then, if it remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends a high pulse.
            new_pls_strength = not all(inputs.values())
            for mod_target in mod_targets:
                stack.append((mod_target, new_pls_strength, pls_target))
    return output


@print_function
def main(input: str) -> int:
    lines = input.split('\n')
    # Store the input in a dict
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
        if 'rx' in targets:
            rx_source = mod_name
        for pls_target in targets:
            if pls_target in modules:
                modules[pls_target][3][mod_name] = False
    # Process the button press
    low_tot, hi_tot = 0, 0
    idx = 0
    rx_ping_idxs = {}
    ans_p1, ans_p2 = None, None
    while True:
        idx += 1
        low, hi, rx_ping_names = press_button(modules, rx_source)
        low_tot += low
        hi_tot += hi
        if idx == 1_000:
            ans_p1 = low_tot * hi_tot
        # Record idxs in which the rx_source got pinged by its various sources
        for name in rx_ping_names:
            if name not in rx_ping_idxs:
                rx_ping_idxs[name] = idx
        # Once pinged by all, we look for the soonest they all sync up. We assume a cycle starting 
        # at 0
        if len(rx_ping_idxs) == len(modules[rx_source][3]):
            ans_p2 =math.lcm(*rx_ping_idxs.values())
        if ans_p1 and ans_p2:
            return (ans_p1, ans_p2)


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    input = sys.stdin.read().strip()
    print('  ->', main(input) == (AOC_ANSWER[0], AOC_ANSWER[1]))


