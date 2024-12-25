"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import re

AOC_ANSWER = ('1,5,7,4,1,6,0,3,0', 108107574778365)


def solve(A: int, program: list[int]):
    """
    Generates the output for a given program and A value. If only_first is True, only the first 
    output will be generated.
    Felt like being fancy so I made a generator.
    """
    B, C, idx = 0, 0, 0
    while idx < len(program):
        opcode = program[idx]
        operand = program[idx+1]
        combo_operand = [0, 1, 2, 3, A, B, C][operand]
        match opcode:
            case 0:
                A >>= combo_operand
            case 1:
                B = B ^ operand
            case 2:
                B = combo_operand % 8
            case 3:
                if A:
                    idx = operand - 2
            case 4:
                B = B ^ C
            case 5:
                yield combo_operand % 8
            case 6:
                B = A >> combo_operand
            case 7:
                C = A >> combo_operand
        idx += 2


@print_function
def part_one(input_txt: str) -> int:
    """
    We're asked to apply a sequence of operations on a number.
    """
    A, _, _, *program = map(int, re.findall('\\d+', input_txt))
    return ','.join(map(str, solve(A, program)))


@print_function
def part_two(input_txt: str) -> int:
    """
    We need to find the number A which makes the output of the program equal to the program 
    sequence. The number is too large to brute force. However, when analysing the input it can be 
    seen that
    - We are looping. The last operation 3,0 sets the index back to the beginning unless A == 0
    - A is only modified once, at the end of the loop by A //= 8.
    - Therefore, A reduces in size by three bits every loop. In the last loop it is between 0-7
    
    We can calculate reversely. Try which value of 0-7 gives us the last program item, then shift 
    the answer left three bits and find the second to last program item, etc.
    """
    _, _, _, *program = map(int, re.findall('\\d+', input_txt))
    qeue = [(0, 0)]
    answers = []
    while qeue:
        ans, depth = qeue.pop()
        depth -= 1
        if depth == -len(program)-1:
            if list(solve(ans, program)) == program:
                answers.append(ans)
            continue
        ans <<= 3
        target = program[depth]
        for idx in range(8):
            if next(solve(ans + idx, program)) == target:
                qeue.append((ans + idx, depth))
    return min(answers)


@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        part_one(input_txt), 
        part_two(input_txt)
    )

aoc_run( __name__, __file__, main, AOC_ANSWER)
