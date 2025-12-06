"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
from functools import reduce
import re
import operator

AOC_ANSWER = (5877594983578, 11159825706149)

OPERATOR = {
    '+': operator.add,
    '*': operator.mul,
}

@print_function
def part_one(input_txt: str) -> int:
    lines = input_txt.split('\n')
    operators = re.findall('[\\*\\+]', lines.pop())
    numbers = tuple(map(int, re.findall('\\d+', line)) for line in lines)
    score = 0
    for op, nums in zip(operators, zip(*numbers)):
        score += reduce(OPERATOR[op], nums)
    return score


@print_function
def part_two(input_txt: str) -> int:
    lines = input_txt.split('\n')
    operators = lines.pop()
    col = 0
    score = 0
    # Scan over all columns (column index indicated by col) untill an operator is encountered. Then
    # scan over the other lines one digit at a time to generate the numbers, then score them 
    # similarly to part 1.
    while True:
        # Increment column index (col) untill we align with an operator.
        while col < len(operators) and operators[col] == ' ':
            col += 1
        # Make sure we don't end up out of bounds
        if col == len(operators):
            break
        op = operators[col]
        # Scan over the other lines to generate one number per column. Stop once an empty column is 
        # found
        nums = []
        while col < len(operators):
            num_txt = ''.join(line[col] for line in lines).strip()
            if num_txt:
                nums.append(int(num_txt))
            else:
                break
            col += 1
        # Score the numbers similarly to part 1
        score += reduce(OPERATOR[op], nums)
    return score


@print_function
def part_two_faster(input_txt: str) -> int:
    """
    Another variant. ChatGPT suggested in code review to do transposing beforehand to prevent 
    reslicing. This reduces run time from 1.5ms to 0.6ms. A large relative but small absolute 
    improvement
    """
    lines = input_txt.split('\n')
    operators = lines.pop()
    transposed = list(''.join(a).strip() for a in zip(*lines))
    score = 0
    problem_score = 0
    problem_op = None
    for op, num in zip(operators, transposed):
        if op != ' ':
            problem_op = OPERATOR[op]
            if op == '+':
                problem_score = 0
            else:
                problem_score = 1
        if num:
            problem_score = problem_op(problem_score, int(num))
        else:
            score += problem_score
            problem_score = None
    score += problem_score
    return score


@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        part_one(input_txt), 
        part_two(input_txt)
    )

aoc_run( __name__, __file__, main, AOC_ANSWER)
