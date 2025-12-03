"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
from collections import deque

AOC_ANSWER = (46978532, 163035127721)


def move_p1(cups: list[int]):
    pick_up = [cups.pop(1) for _ in range(3)]
    sorted_cups = list(sorted(cups))
    dest = sorted_cups[sorted_cups.index(cups[0])-1]
    dest_idx = cups.index(dest)
    cups = cups[1:dest_idx+1] + pick_up + cups[dest_idx+1:] + cups[:1]
    return cups


def score_cups_p1(cups: list[int]) -> int:
    idx = cups.index(1)
    return int(''.join(str(ch) for ch in (cups[idx+1:] + cups[:idx])))


@print_function
def part_one(input_txt: str) -> int:
    cups = list(map(int, list(input_txt)))
    for _ in range(100):
        cups = move_p1(cups)
    return score_cups_p1(cups)


def solve_p2(cups: list[int], iterations: int, full_output: bool) -> list[int]:
    """
    Solves the reordering of cups after a variable number of iterations. The code is optimized for 
    very large (1E7) number of cups by using a double-ended queu (deque) and putting aside the 
    picked-up cup sets untill their destinations are encountered.

    While faster, this still takes ±3s to run in pypy.
    
    :param cups: List of integers of cups
    :type cups: list[int]
    :param iterations: Number of iterations to perform
    :type iterations: int
    :param full_output: True if the full output is required (p1) False if only 1 and its two 
    following cups are enough
    :type full_output: bool
    :return: returns a (partial or full) list of cup values.
    :rtype: list[int]
    """
    queu = deque(cups)
    max_val = max(cups)
    to_place: dict[int, list[int]] = {}
    # Generate the simulation. When items are picked up, don't place them untill you run into their
    # destination. This saves time by not having to reslice the list every round.
    for idx in range(iterations):
        # Get the leftmost value. If picked up values need to be inserted afterwards, do so
        val = queu.popleft()
        if val in to_place:
            values_to_insert = to_place.pop(val)
            queu.extendleft(reversed(values_to_insert))
        # Pick up values one-by-one. If picked up values need to be inserted afterwards, do so
        picked_up = []
        while len(picked_up) < 3:
            nval = queu.popleft()
            if nval in to_place:
                values_to_insert = to_place.pop(nval)
                queu.extendleft(reversed(values_to_insert))
            picked_up.append(nval)
        # Calculate the destination. This should loop-around from 1 to the max value
        dest = (val - 2) % max_val + 1
        while dest in picked_up:
            dest = (dest - 2) % max_val + 1
        # Store the section to place it later
        to_place[dest] = picked_up
        # Add the value to the right of the queu
        queu.append(val)
    
    # Generating the full output can be extremely slow for large datasets.
    if full_output:
        # Place all remaining placeholders and return the output as a list of ints.
        output = list(queu)
        while to_place:
            for key in list(to_place):
                if key in output:
                    idx = output.index(key)
                    values_to_insert = to_place.pop(key)
                    output = output[:idx+1] + values_to_insert + output[idx+1:]
    else:
        # Calculate the two characters after 1. This is done recursively in a while loop. A function
        # could have the same effect but it would need to be defined within this function. Recursion
        # is necessary as for each cup that is added we need to consider whether that was the 
        # destination of another previously picked up set of cups.
        to_place[0] = list(queu)
        output = []
        stack = [(1, True)]
        while stack and len(output) < 3:
            last_val, add_val = stack.pop() # gets last 
            if add_val:
                output.append(last_val)
            # If 'last_val' was the destination of previously picked up cups, we can append these to 
            # the output and find the values that follow it.
            if last_val in to_place:
                for num in reversed(to_place[last_val]):
                    stack.append((num, True))
                continue
            # if 'last_val' is part of picked up cups, we can add the cups that follow it and then 
            # continue looking after the destination of those cups.
            for key, val in to_place.items():
                if last_val not in val:
                    continue
                idx = val.index(output[-1])
                stack.append((key, False))
                for num in reversed(val[idx+1:]):
                    stack.append((num, True))
                break
    # Finally we return the (partial or complete) output
    return output


@print_function
def part_two(input_txt: str) -> int:
    """"
    The code from p1 could quickly run for 10M iterations for length 10, but for length 1M it takes
    too long (±2 days). Instead we optimize our solution
    """
    cups = list(map(int, list(input_txt)))
    cups = cups + list(range(max(cups) + 1, 1_000_000 + max(cups) + 1 - len(cups)))
    cups = solve_p2(cups, 10_000_000, False)
    return cups[1] * cups[2]


@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        part_one(input_txt), 
        part_two(input_txt)
    )

aoc_run( __name__, __file__, main, AOC_ANSWER)
