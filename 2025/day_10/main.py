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
import z3

AOC_ANSWER = (530, 20172)


@print_function
def part_one(input_txt: str) -> int:
    lines = input_txt.split('\n')
    score_p1 = 0
    for line in lines:
        # Parse input
        parts = line.split(' ')
        diagram = parts[0][1:-1]
        diagram = tuple(char == '#' for char in diagram)
        buttons = [list(map(int, part[1:-1].split(','))) for part in parts[1:-1]]
        # joltage = tuple(map(int, parts[-1][1:-1].split(',')))
        # Broad-first-search (BFS) over which buttons to press untill we find one leading to the 
        # correct machine settings
        start = (False, ) * len(diagram)
        stack = deque([(0, start)])
        seen = set()
        while True:
            steps, pos = stack.popleft()
            if diagram == pos:
                score_p1 += steps
                break
            if pos in seen:
                continue
            seen.add(pos)
            for button in buttons:
                new_pos = tuple(p != (idx in button) for idx, p in enumerate(pos))
                stack.append((steps + 1, new_pos))
    return score_p1


@print_function
def part_two(input_txt: str) -> int:
    """
    Solved with Z3 arithmatic solver. I hate it with a passion, but it is very strong and 
    surprisingly fast.

    Z3 defines a set of algebraic equations which it solves algebraically. 
    """
    lines = input_txt.split('\n')
    score_p2 = 0
    for line in lines:
        # Parse input
        parts = line.split(' ')
        buttons = [list(map(int, part[1:-1].split(','))) for part in parts[1:-1]]
        joltage = tuple(map(int, parts[-1][1:-1].split(',')))
        # Z3 bullshit start here. I hate it I hate it I hate it I hate it
        # z3.Optimize is a class to which we can add constraints for the solution. Later it can 
        # optimize the solution for either a min or max function.
        solver = z3.Optimize()
        # Iterate over all buttons, x_idx is a variable indicating how often button_idx is pressed.
        # Each x_idx should be a positive integer.
        button_vars = []
        no_presses = 0
        for idx, button in enumerate(buttons):
            var = z3.Int(f'x_{idx}')
            solver.add(var >= 0)
            button_vars.append(var)
            no_presses += var
        # Add the constraint for each joltage requirement
        for jolt_idx, jolt_value in enumerate(joltage):
            eq = 0
            for button, var in zip(buttons, button_vars):
                if jolt_idx in button:
                    eq += var
            solver.add(eq == jolt_value)
        # Add the function to minimize
        solver.minimize(no_presses)
        # The model is only computed when we run the check() method. It returns z3.sat if a solution
        # is found
        assert solver.check() == z3.sat
        # Retreiving model parameters is not straightforward. The model() method returns the model 
        # form which the arguments can be retreived using []. Then they are converted to ints using
        # as_long()
        model = solver.model()
        steps = sum(model[arg].as_long() for arg in button_vars)
        score_p2 += steps
        
    return score_p2



@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        part_one(input_txt), 
        part_two(input_txt)
    )

aoc_run( __name__, __file__, main, (7, 33), 'ex')
aoc_run( __name__, __file__, main, AOC_ANSWER)
