"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run, tuple_sub
from functools import cache

AOC_ANSWER = (107934, 130470079151124)

NUMPAD_POS = {
    '7': (0, 0),
    '8': (0, 1),
    '9': (0, 2),
    '4': (1, 0),
    '5': (1, 1),
    '6': (1, 2),
    '1': (2, 0),
    '2': (2, 1),
    '3': (2, 2),
    '0': (3, 1),
    'A': (3, 2),
}

DIRPAD_POS = {
    '^': (0, 1),
    'A': (0, 2),
    '<': (1, 0),
    'v': (1, 1),
    '>': (1, 2),
}

@cache
def numeric_keypad(target: str, start: str = 'A') -> list[tuple[str]]:
    """
    Calculates all possible options (= a tuple of strings with each string equal to <, >, ^ or v) 
    which would result in a button press of target (= a string indicating the button to press) when
    the current position is start (= a string indicating the button previously pressed).

    Position (row, column)
          0   1   2
        +---+---+---+
      0 | 7 | 8 | 9 |
        +---+---+---+
      1 | 4 | 5 | 6 |
        +---+---+---+
      2 | 1 | 2 | 3 |
        +---+---+---+
      3     | 0 | A |
            +---+---+
    """
    target_pos = NUMPAD_POS[target]
    start_pos = NUMPAD_POS[start]
    dpos = tuple_sub(target_pos, start_pos)
    moves = ['v' for _ in range(dpos[0])] + ['^' for _ in range(-dpos[0])] \
        + ['>' for _ in range(dpos[1])] + ['<' for _ in range(-dpos[1])]
    permutations = [tuple(moves) + ('A',), tuple(reversed(moves)) + ('A',)]
    # Remove corner option when moving from bottom right to top left
    if 3 == start_pos[0] and 0 == target_pos[1]:
        permutations.remove(('<',) * -dpos[1] + ('^',) * -dpos[0] + ('A',))
    # Remove corner option when moving from top left to bottom right
    elif 3 == target_pos[0] and 0 == start_pos[1]:
        permutations.remove(('v',) * dpos[0] + ('>',) * dpos[1] + ('A',))
    return permutations

@cache
def directional_keypad(target: str, start: str = 'A') -> list[tuple[str]]:
    """
    Calculates all possible options (= a tuple of strings with each string equal to <, >, ^ or v) 
    which would result in a button press of target (= a string indicating the button to press) when
    the current position is start (= a string indicating the button previously pressed).

    Position (row, column)
          0   1   2
            +---+---+
      0     | ^ | A |
        +---+---+---+
      1 | < | v | > |
        +---+---+---+
    """
    target_pos = DIRPAD_POS[target]
    start_pos = DIRPAD_POS[start]
    dpos = tuple_sub(target_pos, start_pos)
    moves = ['v' for _ in range(dpos[0])] + ['^' for _ in range(-dpos[0])] \
        + ['>' for _ in range(dpos[1])] + ['<' for _ in range(-dpos[1])]
    permutations = [tuple(moves) + ('A',), tuple(reversed(moves)) + ('A',)]
    if 0 == start_pos[0] and 0 == target_pos[1]:
        # Remove corner option when moving from top right to bottom left
        permutations.remove(('<',) * -dpos[1] + ('v',) * dpos[0] + ('A',))
    elif 0 == target_pos[0] and 0 == start_pos[1]:
        # Remove corner option when moving from top left to bottom right
        permutations.remove(('^',) * -dpos[0] + ('>',) * dpos[1] + ('A',))
    return permutations


@cache
def process_direction_press(target: str, source: str, depth: int) -> int:
    """
    Calculates the minimally required number of steps to press a directional button on the final 
    robot of a connected set of {depth} robots. Is called recursively.
    """
    # Calculate in how many way we can press the target at depth-1
    key_press_options = directional_keypad(target, source)
    if depth == 1:
        return min(len(row) for row in key_press_options)
    else:
        # Call recursively at depth-1 for each option
        key_press_lengths = []
        for key_press_option in key_press_options:
            source = 'A'
            current_length = 0
            for target in key_press_option:
                current_length += process_direction_press(target, source, depth - 1)
                source = target
            key_press_lengths.append(current_length)
        return min(key_press_lengths)


@cache
def process_character(code, start = 'A', depth = 2):
    """
    Processes one character in the code. Depth indicates the number of directional keypads operating
    robots.
    """    
    # Find the options for directional moves for the final robot
    key_press_options = [tuple()]
    for target in code:
        new_key_presses = numeric_keypad(target, start)
        key_press_options = [old_keys + new_keys for old_keys in key_press_options for new_keys in new_key_presses]
        start = target
    # Calculate the number of steps required for each of these directional options
    key_press_lengths = []
    for code in key_press_options:
        new_len = 0
        start = 'A'
        for target in code:
            new_len += process_direction_press(target, start, depth)
            start = target
        key_press_lengths.append(new_len)
    return min(key_press_lengths)

@print_function
def solve(input_txt: str, depth: int) -> int:
    """"""
    codes = input_txt.split('\n')
    ans = 0
    for code in codes:
        shortest_len = 0
        start = 'A'
        for char in code:
            shortest_len += process_character(char, start, depth)
            start = char
        ans += shortest_len * int(code[:-1])
    return ans

@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        solve(input_txt, 2), 
        solve(input_txt, 25)
    )
aoc_run(__name__, __file__, main, AOC_ANSWER)


