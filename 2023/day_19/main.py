"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2
# 08:18:14

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
import operator

OPERATORS = {
    '<': operator.__lt__,
    '>': operator.__gt__,
}

# @print_function(include_args=True, run_time=False, start=True)
def is_accepted(part, wfs, wf_name):
    if wf_name == 'R':
        return False
    if wf_name == 'A':
        return True
    for wf in wfs[wf_name]:
        if type(wf) == str:
            return is_accepted(part, wfs, wf)
        attribute, operation, op_value, target = wf
        value = part[attribute]
        if operation(value, op_value):
            return is_accepted(part, wfs, target)
    assert False, 'This code should not be reached'

@print_function()
def part_one(input: str) -> int:
    input_p1, input_p2 = input.split('\n\n')
    
    # print(rules)
    wfs = {} # workflows
    for rule_line in input_p1.split('\n'):
        name, rules_str = re.match('(\w+)\{(.*)\}', rule_line).groups()
        rules = []
        for rule_str in rules_str.split(','):
            mtch = re.match('(\w)([<>])(\d+):(.*)', rule_str)
            if mtch:
                attribute, opperation, value, target = mtch.groups()
                rules.append((attribute, OPERATORS[opperation], int(value), target))
            else:
                rules.append(rule_str)
        wfs[name] = rules
    # pprint(wfs)
        
        
    ans = 0
    for part_str in input_p2.split('\n'):
        part_vals = map(int, re.search('{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}', part_str).groups())
        part = {key: val for key, val in zip('xmas', part_vals)}
        if is_accepted(part, wfs, 'in'):
            ans += sum(part.values())
    return ans






@print_function()
def part_two(input: str) -> int:
    lines = input.split('\n')
# @print_function()
# def main(input: str) -> tuple[int, int]:
#     return (part_one(input), part_two(input))
if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    input = sys.stdin.read().strip()
    print(part_one(input) == AOC_ANSWER[0])
    print(part_two(input) == AOC_ANSWER[1])
    # print('  ->', main(input) == (AOC_ANSWER[0], AOC_ANSWER[1]))


