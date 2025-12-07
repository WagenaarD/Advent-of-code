"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
from collections import defaultdict

AOC_ANSWER = (1537, 18818811755665)


def tuple_add(*args: tuple[int, ...]) -> tuple[int, ...]:
    """
    Generates an N-dimensional tuple from M N-dimensional tuples. The resulting tuple is the sum 
    along of the N dimensions.
    
    :param args: M arguments of N-dimensional tuples.
    :return: A tuple of N-dimensions with the summed value along all arguments
    :rtype: tuple
    """
    return tuple(sum(axis) for axis in zip(*args))


@print_function
def part_one(input_txt: str) -> int:
    lines = input_txt.split('\n')
    splitters = set()
    for row, line in enumerate(lines):
        if 'S' in line:
            start = (row, line.index('S'))
        splitters.update((row, col) for col, char in enumerate(line) if char == '^')
    stack = [start]
    seen = set()
    while stack:
        pos = stack.pop()
        # Don't extend beyond the grid
        if pos[0] >= len(lines):
            continue
        # Don't recalculate paths
        if pos in seen:
            continue
        seen.add(pos)
        if pos in splitters:
            # When on a splitter, add the lateral sides
            for dpos in ((1, -1), (1, 1)):
                npos = tuple_add(pos, dpos)
                stack.append(npos)
        else:
            # When not on a splitter, move down one cell
            npos = tuple_add(pos, (1, 0))
            stack.append(npos)
    return len(splitters & seen)


@print_function
def main(input_txt: str) -> tuple[int, int]:
    """
    """
    # Code assumes we can move diagonal after a splitter. This was true for my input
    assert '^^' not in input_txt, 'We assume diagonal movement after splitter (True for my input).'
    # Parse input
    lines = input_txt.split('\n')
    splitters = set()
    for row, line in enumerate(lines):
        if 'S' in line:
            start = (row, line.index('S'))
        splitters.update((row, col) for col, char in enumerate(line) if char == '^')
    # We move keep track of all paths, one row at a time. For each path we keep track of its weight
    # (= the number of paths which it represents). Once a path gets out of bounds, we add its weight
    # to the score. Simultaneously we keep track of the seen splitters, which answers p1.
    stack = defaultdict(int)
    stack[start] += 1
    score_p2 = 0
    seen_splitters = set()
    while stack:
        # Go through the stack, one layer at a time
        new_stack = defaultdict(int)
        for pos, weight in stack.items():
            if pos[0] >= len(lines):
                score_p2 += weight
                continue
            elif pos in splitters:
                seen_splitters.add(pos)
                # When on a splitter, add the lateral sides AND DOWN
                for dpos in ((1, -1), (1, 1)):
                    npos = tuple_add(pos, dpos)
                    new_stack[npos] += weight
            else:
                # When not on a splitter, move down one cell
                npos = tuple_add(pos, (1, 0))
                new_stack[npos] += weight
        stack = new_stack
    score_p1 = len(seen_splitters)
    return score_p1, score_p2


aoc_run( __name__, __file__, main, AOC_ANSWER)
