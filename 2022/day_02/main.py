"""
Advent of code challenge 2022

Opponent moves:
A: Rock
B: Paper
C: Scissors

Move scores (Part 1 character):
X: Rock     (score 1)
Y: Paper    (score 2)
Z: Scissors (score 3)

Win scores (Part 2 character):
X: Loss: 0
Y: Draw: 3
Z: Win:  6
"""

__project__   = 'Advent of code 2022'
__author__    = 'D W'


def match_string_to_score(match_string: str) -> int:
    """
    Calculates the score based on a single string of format "A X" according to the first elf's
    definition
    """
    assert type(match_string) == str
    assert len(match_string) == 3
    assert match_string[0] in ['A', 'B', 'C']
    assert match_string[1] == ' '
    assert match_string[2] in ['X', 'Y', 'Z']
    
    # Add the move specific score
    if match_string[2] == 'X':
        score = 1
    elif match_string[2] == 'Y':
        score = 2
    elif match_string[2] == 'Z':
        score = 3
    else:
        raise(Exception('WTF: unexpected match_string[2] for {}'.format(match_string)))
    
    # Add the result specific score
    opp_move = ord(match_string[0]) - ord('A')
    your_move = ord(match_string[2]) - ord('X')
    if opp_move == your_move:
        score += 3
    elif your_move - opp_move in [1, -2]:
        score += 6
    
    # Finish up
    return score


def win_loss_string_to_score(match_string: str) -> int:
    """
    Calculates the score based on a single string of format "A X" according to the second elf's
    definition
    """
    assert type(match_string) == str
    assert len(match_string) == 3
    assert match_string[0] in ['A', 'B', 'C']
    assert match_string[1] == ' '
    assert match_string[2] in ['X', 'Y', 'Z']

    # Calculate your move
    opp_move = ord(match_string[0]) - ord('A')
    # X: Loss, Y: Draw, Z: Win
    if match_string[2] == 'X':
        your_move = (opp_move + 2) % 3
        score = 0 + 1 + your_move
    elif match_string[2] == 'Y':
        your_move = opp_move
        score = 3 + 1 + your_move
    elif match_string[2] == 'Z':
        your_move = (opp_move + 1) % 3
        score = 6 + 1 + your_move
    else:
         raise(Exception('WTF: unexpected match_string[2]'))
    
    # Finish up
    return score
        

if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    full_text = open('input.txt').read()
    match_list = full_text.split('\n')

    match_score_list = [match_string_to_score(match) for match in match_list]
    print('Part 1 - Total score according to input: {}'.format(sum(match_score_list)))

    updated_match_score_list = [win_loss_string_to_score(match) for match in match_list]
    print('Part 2 - Total score according to input: {}'.format(sum(updated_match_score_list)))
