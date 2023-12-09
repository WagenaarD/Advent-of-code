"""
Advent of code challenge 2022
"""

__project__   = 'Advent of code 2022'
__author__    = 'D W'

import re


# def line_contains(line: str) -> bool:
#     """
#     Input: a string with four numbers representing two ranges (e.g. 1-4, 5-7).
#     Tests if one of these ranges FULLY contains the other range. This is the case if for one range
#     the low-end is <= the other low_end and the high-end is >= the other high end.
#     """
#     match_list = [int(match) for match in re.findall('[0-9]+', line)]
#     return (match_list[0] <= match_list[2] and match_list[1] >= match_list[3]) or \
#         (match_list[0] >= match_list[2] and match_list[1] <= match_list[3])

    
# def line_has_overlap(line: str) -> bool:
#     """
#     Input: a string with four numbers representing two ranges (e.g. 1-4, 5-7).
#     Tests if one of these ranges has ANY overlap with the other range. This is the case if any 
#     number is present in the other range.
#     """
#     match_list = [int(match) for match in re.findall('[0-9]+', line)]
#     return (match_list[3] >= match_list[0] and match_list[2] <= match_list[0]) or \
#         (match_list[2] <= match_list[1] and match_list[3] >= match_list[1]) or \
#         (match_list[1] >= match_list[2] and match_list[0] <= match_list[2]) or \
#         (match_list[0] <= match_list[3] and match_list[1] >= match_list[3])


# if __name__ == '__main__':
#     """Executed if file is executed but not if file is imported."""
#     input_lines = open('input.txt').read().split('\n')
#     print('Part 1 result: {}'.format([line_contains(line) for line in input_lines].count(True)))
#     print('Part 2 result: {}'.format([line_has_overlap(line) for line in input_lines].count(True)))

# Minimalistic approach
input_lines = open('input.txt').read().split('\n')
# num_list = [[int(match) for match in re.findall('[0-9]+', line)] for line in input_lines]
num_list = [map(int, re.findall('[0-9]+', line)) for line in input_lines] # Suggestion LiquidFun
set_list = [(set(range(num[0], num[1] + 1)), set(range(num[2], num[3] + 1))) for num in num_list]
print('Part 1:', [pair[0] >= pair[1] or pair[0] <= pair[1] for pair in set_list].count(True))
print('Part 2:', [bool(pair[0] & pair[1]) for pair in set_list].count(True))