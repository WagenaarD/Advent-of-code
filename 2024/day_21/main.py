"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run, tuple_sub, tuple_add
from functools import cache

AOC_ANSWER = (107934, 130470079151124)

DIRS = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1),
}

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
def generic_keypad(target: str, start: str, is_directional: bool) -> list[tuple[str]]:
    """
    Calculates all possible options (= a tuple of strings with each string equal to <, >, ^ or v)
    which would result in a button press of target (= a string indicating the button to press) when
    the current position is start (= a string indicating the button previously pressed).

    This function allows for two designs, the directional keypad (is_directional = True) and
    numerical keypad (=False). The only differences are the key to coordinate layour (dir_dict) and
    the coordinate through which travel is forbidden (forbidden).

    Numerical keypad             Directional keypad
          0   1   2                   0   1   2
        +---+---+---+                   +---+---+
      0 | 7 | 8 | 9 |             0     | ^ | A |
        +---+---+---+               +---+---+---+
      1 | 4 | 5 | 6 |             1 | < | v | > |
        +---+---+---+               +---+---+---+
      2 | 1 | 2 | 3 |
        +---+---+---+
      3     | 0 | A |
            +---+---+
    """
    dir_dict = DIRPAD_POS if is_directional else NUMPAD_POS
    forbidden = (0, 0) if is_directional else (3, 0)
    target_pos = dir_dict[target]
    start_pos = dir_dict[start]
    dpos = tuple_sub(target_pos, start_pos)
    moves = ['v' for _ in range(dpos[0])] + ['^' for _ in range(-dpos[0])] \
        + ['>' for _ in range(dpos[1])] + ['<' for _ in range(-dpos[1])]
    permutations = [tuple(moves) + ('A',), tuple(reversed(moves)) + ('A',)]
    # Remove paths travelling through the forbidden coordinate.
    if all(forbidden[idx] in (start_pos[idx], target_pos[idx]) for idx in range(2)):
        pos = start_pos
        for move in moves:
            pos = tuple_add(pos, DIRS[move])
            if pos == forbidden:
                permutations.pop(0)
                break
        else:
            permutations.pop()
    return list(set(permutations))


@cache
def process_direction_press(target: str, source: str, depth: int) -> int:
    """
    Calculates the minimally required number of steps to press a directional button on the final
    robot of a connected set of {depth} robots. Is called recursively.
    """
    # Calculate in how many way we can press the target at depth-1
    key_press_options = generic_keypad(target, source, True)
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
def process_character(code: str, start: str, depth: int) -> int:
    """
    Processes one character in the code. Depth indicates the number of directional keypads operating
    robots.
    """
    # Find the options for directional moves for the final robot
    key_press_options = [tuple()]
    for target in code:
        new_key_presses = generic_keypad(target, start, False)
        key_press_options = [old_keys + new_keys for old_keys in key_press_options
                             for new_keys in new_key_presses]
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

aoc_run( __name__, __file__, main, AOC_ANSWER)
