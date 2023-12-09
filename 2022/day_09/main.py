"""
Advent of code challenge 2022
>> python3 main.py < in
Start   - 08:35
Part 1  - 08:49 - 5874
Part 2  - 10:54 - 2467
Cleanup - 11:08
"""

import sys
import itertools as it
from dataclasses import dataclass, field
from collections import defaultdict
import re
import pprint


DIRECTIONS = {'R': (0, 1), 'L': (0, -1), 'U': (-1, 0), 'D': (1, 0)}


def visualize_snake(snake: list, min_size: int = 5) -> None:
    """
    Not strictly necessary. Prints the position of the snake in a dot grid similar to the exercise
    """
    size = max([max(bit) for bit in snake] + [-min(bit) for bit in snake] + [min_size])
    output = ''
    for row in range(-size, size+1):
        for col in range(-size, size+1):
            if (row, col) in snake:
                if snake[0] == (row, col):
                    output += 'H'
                else:
                    output += str(snake.index((row, col)))
            elif (row, col) == (0, 0):
                output += 's'
            else:
                output += '.'
        output += '\n'
    print(output[:-1])


def track_snake(input, snake_length, log = True):
    """
    Processes commands and tracks the snake position
    """
    is_out_of_bounds = lambda x,y: abs(x[0] - y[0]) > 1 or abs(x[1] - y[1]) > 1
    snake = [(0, 0) for _ in range(snake_length)]
    tail_positions =  {(0, 0)}
    for line in input:
        (command_dir, distance) = line.split()
        dx, dy = DIRECTIONS[command_dir]
        if log:
            print('COMMAND:', line)
        for idx in range(int(distance)):
            head = (snake[0][0] + dx, snake[0][1] + dy)
            snake.insert(0, head)
            for idx in range(0, len(snake) - 2):
                # Our current snake is one too large
                # - snake[idx]: current position of previous piece
                # - snake[idx+1]: old position of previous piece 
                # - snake[idx+2]: old position of next piece
                if not is_out_of_bounds(snake[idx], snake[idx + 2]):
                    # Don't need to move next piece, remove old position of previous piece and break
                    snake.pop(idx + 1)
                    break
                else:
                    # Set snake snake[idx+1] to current position of the next piece and continue
                    diff = tuple((snake[idx][ax] - snake[idx+2][ax]) for ax in range(2))
                    move = tuple((diff[ax] // abs(diff[ax]) if diff[ax] else 0) for ax in range(2))
                    snake[idx+1] = tuple((snake[idx+2][ax] + move[ax] for ax in range(2)))
            else:
                snake.pop(-1)
            tail_positions.add(snake[-1])
        if log:
            visualize_snake(snake)
    return tail_positions
            

if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    input = sys.stdin.read().strip().split('\n')  
    print('Part 1:', len(track_snake(input, 2, len(input) < 20)))
    print('Part 2:', len(track_snake(input, 10, len(input) < 20)))