"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2
# 06:12:33
# 07:02:26

AOC_ANSWER = (108955, 106689)

import sys
sys.path.append('../..')
from aoc_tools import *
import itertools as it
from dataclasses import dataclass, field
from collections import defaultdict
import re
import numpy as np
from pprint import pprint
from functools import cache
import math

# north, then west, then south, then east. 
TILT_DIRS = (
    (-1,  0), # North, neg row
    ( 0, -1), # West, neg col
    ( 1,  0), # South, pos row
    ( 0,  1), # East, pos col
)
SORT_SETTINGS = {
    (-1,  0): {'reverse': False, 'key': lambda x: x[0]}, 
    ( 0, -1): {'reverse': False, 'key': lambda x: x[1]}, 
    ( 1,  0): {'reverse': True,  'key': lambda x: x[0]}, 
    ( 0,  1): {'reverse': True,  'key': lambda x: x[1]}, 
}
NO_CYCLES = 1_000_000_000

def calc_load(rounds: list[tuple[int, int]], dims: tuple[int, int]) -> int:
    return sum([dims[0] - r for r, c in rounds])

def apply_tilt(rounds: list[tuple[int, int]], cubes: set[tuple[int, int]], dims: tuple[int, int], 
               t_dir: tuple[int, int]):
    """
    Mutates rounds (returns by argument). Needs to be sped up. Caching is not very useful
    """
    rounds.sort(reverse = sum(t_dir) == 1)
    dr, dc = t_dir
    for idx, (r, c) in enumerate(rounds):
        while True:
            r += dr
            c += dc
            if not (0 <= r < dims[0] and 0 <= c < dims[1]):
                break
            if (r, c) in cubes: # cubes as a set saves time
                break
            if (r, c) in rounds[:idx]: # [:idx] saves time
                break
        rounds[idx] = (r - dr, c - dc)


@print_function()
def apply_cycle(rounds: list[tuple[int, int]], cubes: set[tuple[int, int]], 
                dims: tuple[int, int]) -> None:
    """
    Applies four tilts
    """
    for t_dir in TILT_DIRS:
        apply_tilt(rounds, cubes, dims, t_dir)


def visualize(rounds: list[tuple[int, int]], cubes: set[tuple[int, int]], 
              dims: tuple[int, int]) -> None:
    """
    Visualization only.
    """
    print(f'Score: {calc_load(rounds, dims)}')
    for r in range(dims[0]):
        line = ''
        for c in range(dims[1]):
            if (r, c) in rounds:
                line += 'O'
            elif (r, c) in cubes:
                line += '#'
            else:
                line += '.'
        print(line)
    print('')

def part_one(rounds: list, cubes: set[tuple[int, int]], dims: tuple[int, int]) -> int:
    apply_tilt(rounds, cubes, dims, TILT_DIRS[0])
    return calc_load(rounds, dims)

def part_two(rounds: list, cubes: set[tuple[int, int]], dims: tuple[int, int]) -> int:
    """
    Look for a repetition in the pattern. After each cycle store the rounds positions and check if
    the current pattern has occured before. If it did, any integer number of pattern_lengths can
    be skipped so that only the modulus of the number of cycles remaining and the pattern length
    needs to be applied.
    """
    # Apply cycles untill repetition is found
    known_rounds = {}
    for idx in range(NO_CYCLES):
        print(f'p2 idx = {idx}')
        apply_cycle(rounds, cubes, dims)
        t_rounds = tuple(rounds)
        if t_rounds in known_rounds:
            # print(idx, known_rounds[t_rounds])
            break
        known_rounds[t_rounds] = idx
    # Apply remaining cycles
    cycles_remaining = NO_CYCLES - idx - 1
    pattern_length = idx - known_rounds[t_rounds]
    target_idx = known_rounds[t_rounds] + cycles_remaining % pattern_length
    for rounds, idx in known_rounds.items():
        if idx == target_idx:
            return calc_load(rounds, dims)


@print_function()
def main(input: str) -> tuple[int, int]:
    lines = input.split('\n')
    dims = (len(lines), len(lines[0]))
    rounds, cubes = [], set()
    for r, row in enumerate(lines):
        for c, char in enumerate(row):
            if char == 'O':
                rounds.append((r, c))
            elif char == '#':
                cubes.add((r, c))
    # cubes = tuple(cubes)
    return (
        part_one(rounds.copy(), cubes, dims), 
        part_two(rounds.copy(), cubes, dims),
    )

if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    input = sys.stdin.read().strip()
    print('  ->', main(input) == (AOC_ANSWER[0], AOC_ANSWER[1]))


