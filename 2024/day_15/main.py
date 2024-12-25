"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run, tuple_add

AOC_ANSWER = (1414416, 1386070)

DIRS = {
    '^': (-1, 0),
    '>': (0, 1), 
    'v': (1, 0), 
    '<': (0, -1),
}

def visualize_grid(walls, boxes, bot):
    """
    Prints the grid, also works for an expanded grid (part 2). Grid type is determined by checking 
    if column 1 consists of only walls.
    """
    nrows = max(c[0] for c in walls)+1
    ncols = max(c[1] for c in walls)+1
    is_p2 = all((r, 1) in walls for r in range(nrows))
    rows = []
    for idx, r in enumerate(range(nrows)):
        row = [f'{idx:2} ']
        for c in range(ncols):
            pos = (r, c)
            if pos in walls:
                row.append('#')
            elif pos == bot:
                row.append('@')
            elif is_p2:
                if pos in boxes:
                    row.append('[')
                elif (r, c-1) in boxes:
                    row.append(']')
                else:
                    row.append('.')
            else:
                if pos in boxes:
                    row.append('O')
                else:
                    row.append('.')
        rows.append(''.join(row))
    out = '\n'.join(rows)
    print(out)
    return out

def score_boxes(boxes):
    """
    The GPS coordinate of a box is equal to 100 times its distance from the top edge of the map plus 
    its distance from the left edge of the map. 
    """
    return sum(box[0]*100+box[1] for box in boxes)


@print_function
def part_one(input_txt: str) -> int:
    """
    Stores the sprites (walls, boxes and bot) as (r, c) tuples. Iterates over all moves and moved 
    the bot and boxes accordingly
    """
    grid_txt, moves = input_txt.split('\n\n')
    moves = moves.replace('\n', '')
    walls, boxes = [], []
    for r, row in enumerate(grid_txt.split('\n')):
        for c, val in enumerate(row):
            if val == '#':
                walls.append((r, c))
            elif val == 'O':
                boxes.append((r, c))
            elif val == '@':
                bot = (r, c)
    # print('\nInitial state:')
    # visualize_grid(walls, boxes, bot)

    for move in moves:
        dpos = DIRS[move]
        idx_to_move = []
        pos = bot
        # Scan ahead until you reach a '.' or a '#'. Move only when finding a '.'
        while True:
            pos = tuple_add(pos, dpos)
            if pos in boxes:
                idx_to_move.append(boxes.index(pos))
            elif pos in walls:
                # Encountered a '#'. Stop and dont move
                break
            else:
                # Encountered a '.'. Move the first box to the last position
                bot = tuple_add(bot, dpos)
                if bot in boxes:
                    boxes[boxes.index(bot)] = pos
                break
        # print(f'\nMove {move}:')
        # visualize_grid(walls, boxes, bot)
    return score_boxes(boxes)


@print_function
def part_two(input_txt: str) -> int:
    """
    Stores the sprites (walls, boxes and bot) as (r, c) tuples. Columns are doubled and walls are
    stored twice. Boxes are only stored in their leftmost position.
    """
    grid_txt, moves = input_txt.split('\n\n')
    moves = moves.replace('\n', '')
    walls, boxes = [], []
    bot = (0, 0)
    for r, row in enumerate(grid_txt.split('\n')):
        for c, val in enumerate(row):
            if val == '#':
                walls.append((r, c*2))
                walls.append((r, c*2+1))
            elif val == 'O':
                boxes.append((r, c*2))
            elif val == '@':
                bot = (r, c*2)
    # print('\nInitial state:')
    # visualize_grid(walls, boxes, bot)

    for move in moves:
        dpos = DIRS[move]
        box_idxs_to_move = set()
        places_to_check = [bot]
        while places_to_check:
            # pos is the position for which we will check if it CAN move, npos its destination.
            pos = places_to_check.pop()
            npos = tuple_add(pos, dpos)
            # bos_pos is the left-position of the box that npos collides with (if any)
            box_pos = None
            if npos in boxes:
                box_pos = npos
            elif tuple_add(npos, (0, -1)) in boxes:
                box_pos = tuple_add(npos, (0, -1))
            if box_pos:
                box_idxs_to_move.add(boxes.index(box_pos))
                # For horizontal shifts, we only add one new position to check. For > it is the
                # right position and < it is the left position. For vertical shifts we add both
                # cells
                if move == '>':
                    places_to_check.append(tuple_add(box_pos, 
                        dpos))
                elif move == '<':
                    places_to_check.append(box_pos)
                else:
                    places_to_check.append(box_pos)
                    places_to_check.append(tuple_add(box_pos, (0, 1)))
                continue
            elif npos in walls:
                break
        else:
            # The while loop did not break, so we can process all moves
            for idx in box_idxs_to_move:
                boxes[idx] = tuple_add(boxes[idx], dpos)
            bot = tuple_add(bot, dpos)
        # print(f'\nMove {move}:')
        # visualize_grid(walls, boxes, bot)
    return score_boxes(boxes)


@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        part_one(input_txt), 
        part_two(input_txt)
    )

aoc_run( __name__, __file__, main, AOC_ANSWER, 'ex3')
