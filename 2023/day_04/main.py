"""
Advent of code challenge 2023
>> python3 main.py < in
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2
# 07:59:34
# 08:04:15
# 08:13:14  13:40   07:08

import sys
sys.path.append('..')
from aoc_tools import print_function

AOC_ANSWER = (21485, 11024379)

@print_function()
def main(input: str) -> 'tuple(int, int)':
    lines = input.split('\n')
    score_p1, score_p2 = 0, [1] * len(lines)
    for idx, line in enumerate(lines):
        left, right = line.split(': ')[1].split('|')
        correct = len(set(left.split()) & set(right.split()))
        if correct:
            score_p1 += 2 ** (correct - 1)
        for idx2 in range(idx+1, idx+correct+1):
            score_p2[idx2] += score_p2[idx]
    return score_p1, sum(score_p2)


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    input = sys.stdin.read().strip()
    print('  ->', main(input) == (AOC_ANSWER[0], AOC_ANSWER[1]))