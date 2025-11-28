"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import operator

operators = {
    '+': operator.add,
    # '-': operator.sub,
    # '/': operator.truediv,
    '*': operator.mul,
}

AOC_ANSWER = (4940631886147, 283582817678281)

def solve_equation(equation: tuple[str], advanced_math: bool) -> int:
    """
    Solve equations using elf-math in which everything is evaluated left-to-right regardless of the 
    operator (e.g., 4 + 5 * 3 = 9 * 3 = 27).
    When using advanced math (part 2), + is prioritized over *.
    """
    # Return solution
    if len(equation) == 1:
        return int(equation[0])
    # Fix all brackets
    elif '(' in equation:
        # Find the matching closing bracket for the opening bracket
        depth = 0
        start_idx = equation.index('(')
        for idx, char in enumerate(equation):
            if char == '(':
                depth += 1
            if char == ')':
                if depth == 1:
                    end_idx = idx
                    break
                depth -= 1
        else:
            raise(Exception(f'WTF: Bracket not closed in {equation=}'))
        sub_equation = equation[start_idx+1:end_idx]
        sub_equation_ans = solve_equation(sub_equation, advanced_math)
        new_equation = equation[:start_idx] + (sub_equation_ans, ) + equation[end_idx+1:]
        return solve_equation(new_equation, advanced_math)
    # Prioritize '+' for p2
    elif advanced_math and '+' in equation:
        idx = equation.index('+')
        sub_equation_ans = int(equation[idx-1]) + int(equation[idx+1])
        new_equation = equation[:idx-1] + (sub_equation_ans, ) + equation[idx+2:]
        return solve_equation(new_equation, advanced_math)
    # Do one operation
    else:
        num_1, op, num_2 = equation[0:3]
        ans = operators[op](int(num_1), int(num_2))
        new_equation = (ans, ) + equation[3:]
        return solve_equation(new_equation, advanced_math)
        
@print_function
def main(input_txt: str) -> int:
    lines = input_txt.split('\n')
    score_p1, score_p2 = 0, 0
    for line_txt in lines:
        equation = tuple(line_txt.replace(' ', ''))
        score_p1 += solve_equation(equation, False)
        score_p2 += solve_equation(equation, True)
    return score_p1, score_p2


aoc_run( __name__, __file__, main, AOC_ANSWER)
