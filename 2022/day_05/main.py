"""
Advent of code challenge 2022

Chose to not use error catching, input asserts and functions today.

Start:   12:27
Part 1:  12:56 - QPJPLMNNR
Part 2:  12:58 - BQDNWJPVJ
Cleanup: 13:08

"""

__project__   = 'Advent of code 2022'
__author__    = 'D W'

import copy

(state_input, moves_input) = open('input.txt').read().split('\n\n')

# Process the state input. state_1 is for part_1, state_2 for part_2
state_1 = [[] for _ in range((state_input.find('\n') + 1) // 4)]
for line in state_input.split('\n')[:-1]:
    for idx in range(1, len(line), 4):
        if line[idx] != ' ':
            state_1[idx // 4].append(line[idx])
state_2 = copy.deepcopy(state_1)

# Process moves
for move in moves_input.split('\n'):
    (num_to_move, from_stack, to_stack) = [int(num) for num in move.split() if num.isdigit()]
    state_1[to_stack - 1] = state_1[from_stack - 1][:num_to_move][::-1] + state_1[to_stack - 1]
    state_2[to_stack - 1] = state_2[from_stack - 1][:num_to_move] + state_2[to_stack - 1]
    del state_1[from_stack - 1][:num_to_move]
    del state_2[from_stack - 1][:num_to_move]

# Return result
print('Part 1 result: {}'.format(''.join([stack[0] for stack in state_1])))
print('Part 2 result: {}'.format(''.join([stack[0] for stack in state_2])))
