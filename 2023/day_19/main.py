"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2
# 08:18:14
# Forgot
# 10:20:41 (Work in between)

AOC_ANSWER = (446517, 130090458884662)

import sys
sys.path.append(AOC_BASE_PATH := '/'.join(__file__.replace('\\', '/').split('/')[:-3]))
from aoc_tools import print_function, aoc_run
import re
import math
import operator

OPERATORS = {
    '<': operator.__lt__,
    '>': operator.__gt__,
}

def is_accepted(part, wfs, wf_name):
    """
    Recursive function that tests for acceptance of a part.
    """
    if wf_name == 'R':
        return False
    if wf_name == 'A':
        return True
    for wf in wfs[wf_name]:
        if type(wf) == str:
            return is_accepted(part, wfs, wf)
        attribute, operation, op_value, target = wf
        value = part[attribute]
        if OPERATORS[operation](value, op_value):
            return is_accepted(part, wfs, target)
    assert False, 'This code should not be reached'


def part_one(wfs: dict[list], part_strings: list[str]) -> int:
    """

    """
    ans = 0
    for part_str in part_strings:
        part_vals = map(int, re.search('{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}', part_str).groups())
        part = {key: val for key, val in zip('xmas', part_vals)}
        if is_accepted(part, wfs, 'in'):
            ans += sum(part.values())
    return ans


def part_two(wfs: dict[list]) -> int:
    """
    In part two we need to calculate with ranges. Worked on the first go, but had the stack range 
    from 0-4000 instead of 1-4000. Took a few tens of minutes to debug.
    """
    stack = [({key: 1 for key in 'xmas'}, {key: 4000 for key in 'xmas'},'in', 0)]
    ans = 0
    while stack:
        min_vals, max_vals, workflow_name, workflow_depth = stack.pop()
        if any(min_vals[att] > max_vals[att] for att in 'xmas'):
            continue
        if workflow_name == 'R':
            continue
        if workflow_name == 'A':
            ans += math.prod(max_vals[att] - min_vals[att] + 1 for att in 'xmas')
            continue
        workflow = wfs[workflow_name][workflow_depth]
        if type(workflow) == str:
            # If command is a string, the whole string is moved
            stack.append((min_vals, max_vals, workflow, 0))
            continue
        attribute, operation, op_value, target = workflow
        if operation == '<':
            # Range that matches criteria
            max_vals_split = max_vals.copy()
            max_vals_split[attribute] = op_value - 1
            stack.append((min_vals.copy(), max_vals_split, target, 0))
            # Range that does not match criteria
            min_vals_split = min_vals.copy()
            min_vals_split[attribute] = op_value
            stack.append((min_vals_split, max_vals, workflow_name, workflow_depth + 1))
            continue
        elif operation == '>':
            # Range that matches criteria
            min_vals_split = min_vals.copy()
            min_vals_split[attribute] = op_value + 1
            stack.append((min_vals_split, max_vals.copy(), target, 0))
            # Range that does not match criteria
            max_vals_split = max_vals.copy()
            max_vals_split[attribute] = op_value
            stack.append((min_vals, max_vals_split, workflow_name, workflow_depth + 1))
        else:
            assert False, 'Code assumed unreachable'
    return ans


@print_function
def main(input: str) -> tuple[int, int]:
    input_p1, input_p2 = input.split('\n\n')
    wfs = {} # workflows
    for rule_line in input_p1.split('\n'):
        name, rules_str = re.match('(\w+)\{(.*)\}', rule_line).groups()
        rules = []
        for rule_str in rules_str.split(','):
            mtch = re.match('(\w)([<>])(\d+):(.*)', rule_str)
            if mtch:
                attribute, opperation, value, target = mtch.groups()
                rules.append((attribute, opperation, int(value), target))
            else:
                rules.append(rule_str)
        wfs[name] = rules
    return (part_one(wfs, input_p2.split('\n')), part_two(wfs))


aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')
# aoc_run(__name__, __file__, main, AOC_ANSWER, 'ex')


