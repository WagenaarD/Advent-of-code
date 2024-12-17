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


def solve(A, program, first=False):
    B, C, idx = 0, 0, 0
    output = []
    while idx < len(program):
        opcode = program[idx]
        operand = program[idx+1]
        if operand < 4:
            combo_operand = operand
        elif operand < 7:
            combo_operand = [A, B, C][operand-4]
        else:
            combo_operand = None
        if opcode == 0: # adv
            A = A // (2**combo_operand)
        elif opcode == 1:
            B = B ^ operand
        elif opcode == 2:
            B = combo_operand % 8
        elif opcode == 3:
            if A != 0:
                idx = operand - 2
        elif opcode == 4:
            B = B ^ C
        elif opcode == 5: # out
            if first:
                return combo_operand % 8
            output.append(combo_operand % 8)
        elif opcode == 6: # bdv
            B = A // (2**combo_operand)
        elif opcode == 7: # cdv
            C = A // (2**combo_operand)
        idx += 2
    return output


@print_function
def part_one(input_txt: str) -> int:
    """
    We're asked to apply a sequence of operations on a number.
    """
    register, program = input_txt.split('\n\n')
    register = {key: int(val) for key, val in zip('ABC', re.findall('\\d+', register))}
    program = list(map(int, re.findall('\\d+', program)))
    return ','.join(map(str, solve(register['A'], program)))


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
    _, program_txt = input_txt.split('\n\n')
    program = list(map(int, re.findall('\\d+', program_txt)))
    qeue = [(0, 0)]
    answers = []
    while qeue:
        ans, depth = qeue.pop()
        depth -= 1
        if depth == -len(program)-1:
            if solve(ans, program) == program:
                answers.append(ans)
            continue
        ans <<= 3
        target = program[depth]
        for idx in range(8):
            if solve(ans + idx, program, True) == target:
                qeue.append((ans + idx, depth))
    return min(answers)


@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        part_one(input_txt), 
        part_two(input_txt)
    )
aoc_run(__name__, __file__, main, AOC_ANSWER)
