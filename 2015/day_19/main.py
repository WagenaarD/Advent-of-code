"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in

Input observations:
- There are some 'dead-ends': These atoms can be created, but not changed:
  dead_end_atoms=['C', 'Rn', 'Ar', 'Y']
- All rules create an even number of atoms [2,4,6,8] (and consume 1, incrementing [1,3,5,7]. Total 
required atoms is 274, an increment of 273 thus 39-272 steps are required.
"""
# Start, Part 1, Part 2

AOC_ANSWER = (509, 195)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
from collections import defaultdict
import re
from pprint import pprint
import math
from pprint import pprint
from heapq import heappush

ATOM_RE = 'e|[A-Z][a-z]*'

def find_next_molecules(current: str, rules: tuple[tuple[str, str]]) -> set[str]:
    molecules = set()
    for sub_in, sub_out in rules:
        for match in re.finditer(sub_in, current):
            new = current[:match.span()[0]] + sub_out + current[match.span()[1]:]
            molecules.add(new)
    return molecules

@print_function
def part_one(input: str) -> int:
    rules_txt, input = input.split('\n\n')
    rules = tuple(tuple(rule.split(' => ')) for rule in rules_txt.split('\n'))
    return len(find_next_molecules(input, rules))
 

@print_function
def part_two(input: str) -> int:
    """
    This is not very clean code and I am sorry. I'm also not really sure if it will finish within a 
    decent time for all inputs. Actually I'm quite sure it won't. Also, it just finds AN ANSWER 
    which is not guaranteed to be the best answer, however for my input it was.
    """
    rules_txt, target_txt = input.split('\n\n')
    rules_dct = defaultdict(list)
    for rule in rules_txt.split('\n'):
        atoms = re.findall(ATOM_RE, rule)
        rules_dct[atoms[0]].append(atoms[1:])    
    target_lst = re.findall(ATOM_RE, target_txt)
    dead_end_atoms = [atom for atom in set(target_lst) if not atom in rules_dct]
    # print(f'{dead_end_atoms=}')
    # dead_end_atoms=['C', 'Rn', 'Ar', 'Y']
    rules_txt_lst = rules_txt.split('\n')
    
    # Priority rules
    # Let's consider Rn
    # There are many rules that produce Rn, but none that use it
    # Note the rule: P => SiRnFAr
    # SiRnFAr occurs five times in the solution
    # SiRn could perhaps also be produced in a different way, as some rules produce Si at the end (e.g. N => HSi)
    # RnF could NOT be produced in a different way as NO rules produce F at the front ("> F" not in rule_txt)
    # So we can count the instances of SiRnFAr and replace them with P. Then increment count with number of instances
    # Here we store all priority rules and non-priority rules:
    priority_rules = []
    non_prio_rules = []
    for rule, rule_out_lst in rules_dct.items():
        for rule_out in rule_out_lst:
            rule_out_txt = ''.join(rule_out)
            for dead_end in dead_end_atoms:
                # Look for rules that contain "dead-end" atoms
                if not dead_end in rule_out:
                    continue
                do_replace = False
                # If has prefix atom, check if this can be produced in another way: By rules which 
                # end in prefix atom
                if mtch := re.search(f'({ATOM_RE}){dead_end}', rule_out_txt):
                    prefix_atom = mtch.groups()[0]
                    if not any(rule.endswith(prefix_atom) for rule in rules_txt_lst):
                        do_replace = True
                # If has a succeeding atom, Check if this can be produced in another way: By rules 
                # which start with succeeding character
                if mtch := re.search(f'{dead_end}({ATOM_RE})', rule_out_txt):
                    suffix_atom = mtch.groups()[0]
                    if not any(f'=> {suffix_atom}' in rule for rule in rules_txt_lst):
                        do_replace = True
                # Check if we found a match
                if do_replace:
                    priority_rules.append((rule, rule_out_txt))
                    break
            else:
                non_prio_rules.append((rule, rule_out_txt))
    # We reverse non_prio_rules so the 'e' rules are on top and chosen first
    non_prio_rules = non_prio_rules[::-1]

    # Define dfs
    dfs_cache = {}
    def dfs(target, depth, get_first = True):
        if target in dfs_cache:
            return dfs_cache[target]
        count = 0
        if target == 'e':
            return count
        if 'e' in target:
            return None
        while any(rule_out_txt in target for rule_in, rule_out_txt in priority_rules):
            for rule_in, rule_out_txt in priority_rules:
                rule_count = target.count(rule_out_txt)
                if rule_count:
                    count += rule_count
                    target = target.replace(rule_out_txt, rule_in)
        counts = []
        for rule_in, rule_out_txt in non_prio_rules:
            for mtch in re.finditer(rule_out_txt, target):
                s_idx, e_idx = mtch.span()
                new_target = target[:s_idx] + rule_in + target[e_idx:]
                dfs_result = dfs(new_target, depth + count + 1, get_first)
                if dfs_result != None:
                    if get_first:
                        return dfs_result + count + 1
                    else:
                        counts.append(dfs_result + count + 1)
        if counts:
            dfs_cache[target] = min(counts)
        else:
            dfs_cache[target] = None
        return dfs_cache[target]
    # Execute dfs
    return dfs(target_txt, 0)

@print_function
def main(input: str) -> tuple[int, int]:
    return (
        part_one(input), 
        part_two(input)
    )
aoc_run(__name__, __file__, main, AOC_ANSWER)


