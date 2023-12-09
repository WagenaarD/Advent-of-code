"""
Advent of code challenge 2022
>> python3 main.py < in
Part 1  - 3966 (ex 110)
Part 2  - 933 (ex 20)
"""

import sys
sys.path.insert(0, '/'.join(__file__.replace('\\', '/').split('/')[:-2]))
from _utils.print_function import print_function
import itertools as it


DIRECTIONS = ('NSWE', 'SWEN', 'WENS', 'ENSW')
DIR_CHECK = {
    'N': ((-1, -1), (-1,  1), (-1,  0)), 
    'S': (( 1, -1), ( 1,  1), ( 1,  0)), 
    'W': ((-1, -1), ( 1, -1), ( 0, -1)), 
    'E': ((-1,  1), ( 1,  1), ( 0,  1)), 
}


def print_board(elves):
    """
    Visualization similar to example
    """
    min_row = min([elf[0] for elf in elves])
    max_row = max([elf[0] for elf in elves])
    min_col = min([elf[1] for elf in elves])
    max_col = max([elf[1] for elf in elves])
    for row in range(min_row - 1, max_row + 2):
        output = '{:3} - '.format(row)
        for col in range(min_col - 1, max_col + 2):
            output += '#' if (row, col) in elves else '.'
        print(output)
    print('')


@print_function()
def solve(elves):
    dir_cycle = it.cycle(DIRECTIONS)
    round = 0
    while True:
        round += 1
        new_positions = list()
        dir = next(dir_cycle)
        for row, col in elves:
            # Consider eight cells around. Only move if at least one other elf present
            no_neighbours = sum([(nrow, ncol) in elves \
                for nrow in range(row-1, row+2) for ncol in range(col-1, col+2)]) - 1
            if no_neighbours == 0:
                new_positions.append((row, col, row, col))
                continue
            # Consider all directions
            for dir_key in dir:
                for drow, dcol in DIR_CHECK[dir_key]:
                    if (row + drow, col + dcol) in elves:
                        break
                else:
                    new_positions.append((row + drow, col + dcol, row, col))
                    break
            else:
                # No new position found. Do not move
                new_positions.append((row, col, row, col))
        # Second half of round
        move_targets = [(pos[0], pos[1]) for pos in new_positions]
        elves = list()
        vectors = set()
        for nrow, ncol, row, col in new_positions:
            if move_targets.count((nrow, ncol)) == 1:
                vectors.add((nrow - row, ncol - col))
                elves.append((nrow, ncol))
            else:
                vectors.add((0, 0))
                elves.append((row, col))
        print('== End of Round {} =='.format(round))
        if len(lines) <= 10: print_board(elves)
        if round == 10:
            min_row = min([elf[0] for elf in elves])
            max_row = max([elf[0] for elf in elves])
            min_col = min([elf[1] for elf in elves])
            max_col = max([elf[1] for elf in elves])
            part_1_score = (max_row - min_row + 1) * (max_col - min_col + 1) - len(elves)
        if len(vectors) == 1 and round >= 10:
            break
    return (part_1_score, round)


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    lines = sys.stdin.read().strip().split('\n')
    elves = list()
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == '#':
                elves.append((row, col))
    if len(lines) <= 10: print_board(elves)
    solve(elves)