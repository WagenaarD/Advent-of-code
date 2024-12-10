"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (509, None)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
from aoc_tools import print_loop
import itertools as it
from dataclasses import dataclass, field
from collections import defaultdict, deque, Counter
import re
import numpy as np
from pprint import pprint
from functools import cache
import math
from pprint import pprint

# @cache
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

# def dfs(target: str, current: str, steps: int, rules: tuple[tuple[str, str]]):
#     if sum(1 for c in target if c.isupper()) < sum(1 for c in message if c.isupper()):

# @cache 
def count_molecules(current):
    return sum(1 for c in current if c.isupper())

@print_function
def part_two(input: str) -> int:
    rules_txt, target = input.split('\n\n')
    rules = tuple(tuple(rule.split(' => ')) for rule in rules_txt.split('\n'))
    qeue = deque([('e', 0)])
    target_molecules = count_molecules(target)
    # visited = defaultdict(lambda : math.inf)
    # counts = set()
    idx = 0
    seen = set()
    ## Try BFS, then the first solution is always the best solution
    while qeue:
        current, count = qeue.popleft()
        ## print stuff
        if (idx := idx + 1) % 10_000 == 0:
            # idx_str = f'{idx:,}'.replace(',', '_')
            min_counts = min(c for cc, c in qeue)
            max_counts = max(c for cc, c in qeue)
            n_counts = [sum([c == idx for cc, c in qeue]) for idx in range(min_counts, min_counts+2)]
            progress = n_counts[1] / sum(n_counts)
            print(f'{len(qeue)=:,}, {idx=:,}, counts≥{min_counts}: {progress=:.0%}')
        if current == target:
            print(f'!! {count}')
            return count
        # count += 1
        for molecule in find_next_molecules(current, rules):
            if count_molecules(molecule) > target_molecules:
                continue
            if molecule in seen:
                continue
            seen.add(molecule)
            qeue.append((molecule, count + 1))
    print(count)
    # print(min(counts))
        

class BFS:
    def __init__(self, rules: dict[str, list[list[str]]], dead_ends: list[str]):
        self.rules = rules
        self.dead_ends = dead_ends
        self.pruned = 0

    def solve(self, start: list[str], target: list[str], do_print: bool = False):
        qeue = deque([(start, 0)])
        seen = set()
        loop_idx = 0
        dead_atom_target = ''.join(atom for atom in target if atom in self.dead_ends)
        print(f'{target=}')
        print(f'{self.dead_ends=}')
        print(f'{dead_atom_target=}')
        # return
        ## Try BFS, then the first solution is always the best solution
        while qeue:
            current, steps = qeue.popleft()
            if do_print and (loop_idx := loop_idx + 1) % 10_000 == 0:
                min_counts = min(c for cc, c in qeue)
                n_counts = [sum([c == idx for cc, c in qeue]) for idx in range(min_counts, min_counts+2)]
                progress = n_counts[1] / sum(n_counts)
                print(f'{len(qeue)=:,}, {loop_idx=:,}, counts≥{min_counts}: {progress=:.0%} {self.pruned=}')
            if current == target:
                return steps
            for rule_atom, rule_outs in self.rules.items():
                for atom_idx, atom in enumerate(current):
                    if atom != rule_atom:
                        continue
                    for rule_out in rule_outs:
                        molecule = current[:atom_idx] + rule_out + current[atom_idx+1:]
                        if tuple(molecule) in seen:
                            continue
                        pattern = '.*' + '.*'.join(atom for atom in molecule if atom in self.dead_ends) + '.*'
                        if not re.match(pattern, dead_atom_target):
                            self.pruned += 1
                            continue
                        seen.add(tuple(molecule))
                        qeue.append((molecule, steps + 1))
        return -1



@print_function
def part_two(input: str) -> int:
    rules_txt, target_txt = input.split('\n\n')
    rules = defaultdict(list)
    
    for rule in rules_txt.split('\n'):
        atoms = re.findall('e|[A-Z][a-z]*', rule)
        rules[atoms[0]].append(atoms[1:])
    target = re.findall('e|[A-Z][a-z]*', target_txt)
    dead_end_atoms = [atom for atom in set(target) if not atom in rules]
    # bfs = BFS(rules, dead_end_atoms)
    # return bfs.solve(['e'], target, True)
    
    # OK LETS TRY REVERSE CODING
    # self.dead_ends=['C', 'Rn', 'Ar', 'Y']
    # Let's consider Rn
    # There are many rules that produce Rn, but none that use it
    # Note the rule: P => SiRnFAr
    # SiRnFAr occurs five times in the solution
    # SiRn could perhaps also be produced in a different way, as some rules produce Si at the end (e.g. N => HSi)
    # RnF could NOT be produced in a different way as NO rules produce F at the front ("> F" not in rule_txt)
    # So we can count the instances of SiRnFAr and replace them with P. Then increment count with number of instances
ATOM_RE = 'e|[A-Z][a-z]*'
@print_function
def part_two(input: str) -> int:
    rules_txt, target_txt = input.split('\n\n')
    rules_dct = defaultdict(list)
    for rule in rules_txt.split('\n'):
        atoms = re.findall(ATOM_RE, rule)
        rules_dct[atoms[0]].append(atoms[1:])
    target_lst = re.findall(ATOM_RE, target_txt)
    dead_end_atoms = [atom for atom in set(target_lst) if not atom in rules_dct]
    rules_txt_lst = rules_txt.split('\n')
    
    # REVERSE SOLVE
    old_count, count = -1, 0
    while old_count != count:
        print('another loop')
        count = old_count
        for rule, rule_out_lst in rules_dct.items():
            for rule_out in rule_out_lst:
                rule_out_txt = ''.join(rule_out)
                if rule_out_txt == 'SiRnFAr': print(f'{rule} => {rule_out_txt}')
                # Check if a dead atom is present
                for dead_end in dead_end_atoms:
                    # if rule_out_txt == 'SiRnFAr' and dead_end == 'Rn': print(f'{rule} => {rule_out_txt}')
                    do_replace = False
                    if not dead_end in rule_out:
                        continue
                    if not rule_out_txt in target_txt:
                        continue
                    if rule_out_txt == 'SiRnFAr': print(f'  {dead_end=}')
                    # If has prefix atom
                    if mtch := re.search(f'({ATOM_RE}){dead_end}', rule_out_txt):
                        # Check if this can be produced in another way: By rules which end in prefix atom
                        prefix_atom = mtch.groups()[0]
                        if rule_out_txt == 'SiRnFAr': print(f'    prefix match {prefix_atom}')
                        if not any(rule.endswith(prefix_atom) for rule in rules_txt_lst):
                            if rule_out_txt == 'SiRnFAr': print(f'      unique! setting do_replace = True')
                            do_replace = True
                        else:
                            if rule_out_txt == 'SiRnFAr': print(f'      could be produced in another way...')
                    # If has a succeeding atom
                    if mtch := re.search(f'{dead_end}({ATOM_RE})', rule_out_txt):
                        # Check if this can be produced in another way: By rules which start with succeeding character
                        suffix_atom = mtch.groups()[0]
                        if rule_out_txt == 'SiRnFAr': print(f'    suffix match {suffix_atom}')
                        if not any(f'=> {suffix_atom}' in rule for rule in rules_txt_lst):
                            if rule_out_txt == 'SiRnFAr': print(f'      unique! setting do_replace = True')
                            do_replace = True
                        else:
                            if rule_out_txt == 'SiRnFAr': print(f'      could be produced in another way...')
                    # Check if we found a match
                    if do_replace:
                        occurence = target_txt.count(rule_out_txt)
                        count += occurence
                        print(f'HELL YEAH: {rule} => {rule_out_txt}: {occurence} times in {target_txt=}\nnew {count=}')
                        target_txt = target_txt.replace(rule_out_txt, rule)
    








@print_function
def main(input: str) -> tuple[int, int]:
    return (
        # part_one(input), 
        part_two(input)
    )
aoc_run(__name__, __file__, main, AOC_ANSWER)


