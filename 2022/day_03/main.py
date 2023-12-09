"""
Advent of code challenge 2022
"""

__project__   = 'Advent of code 2022'
__author__    = 'D W'

import string


def get_char_priority(char: str) -> int:
    """
    Every item type can be converted to a priority:
     - Lowercase item types a through z have priorities 1 through 26.
     - Uppercase item types A through Z have priorities 27 through 52.
    """
    return string.ascii_letters.find(char) + 1 


def line_score(backpack: str) -> int:
    """
    Backpack is a string of even lenght of which the first and second halves are considered in 
    different compartments.
    Finds the char that is present in both compartments and returns its priority
    """
    comp_1 = backpack[0:len(backpack) // 2]
    comp_2 = backpack[len(backpack) // 2:]
    for char in comp_1:
        if char in comp_2:
            return get_char_priority(char)
    else:
        raise(Exception('WTF: no char found in both compartments for line: "{}"'.format(backpack)))


def badge_score(backpack_list: list) -> int:
    """
    Finds the char that is present in all three backpacks and returns its priority
    """
    for char in backpack_list[0]:
        if all([char in backpack for backpack in backpack_list[1:]]):
            return get_char_priority(char)
    else:
         raise(Exception('WTF: no badge found in group: "{}"'.format(backpack_list)))


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    text_lines = open('input.txt').read().split('\n')
    
    sum_lines = sum([line_score(line) for line in text_lines])
    print('Part 1 - Total score according to input: {}'.format(sum_lines))
    
    sum_badges = sum([badge_score(text_lines[idx:idx + 3]) for idx in range(0, len(text_lines), 3)])
    print('Part 2 - Total score according to input: {}'.format(sum_badges))
    
   