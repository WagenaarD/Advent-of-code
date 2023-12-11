"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2
# 12:34:10
# 12:58:00
# 13:23:32

AOC_ANSWER = (6613, 511)

import sys
sys.path.append('../..')
from aoc_tools import print_function

# The pipes are arranged in a two-dimensional grid of tiles:
# - | is a vertical pipe connecting north and south.
# - - is a horizontal pipe connecting east and west.
# - L is a 90-degree bend connecting north and east.
# - J is a 90-degree bend connecting north and west.
# - 7 is a 90-degree bend connecting south and west.
# - F is a 90-degree bend connecting south and east.
# - . is ground; there is no pipe in this tile.
# - S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't 
# show what shape the pipe has.

PIPES = {
    '|': {( 1,  0), (-1,  0)},
    '-': {( 0, -1), ( 0,  1)},
    'L': {(-1,  0), ( 0,  1)},
    'J': {(-1,  0), ( 0, -1)},
    '7': {( 1,  0), ( 0, -1)},
    'F': {( 1,  0), ( 0,  1)},
    '.': set(),
}
PRIMARY_AXIS_ADJACENT = ((1, 0), (-1, 0), (0, 1), (0, -1))

@print_function()
def main(input: str) -> int:
    lines = input.split('\n')
    s_pos = [(r, c) for r, row in enumerate(lines) for c, char in enumerate(row) if char == 'S'][0]
    
    # Find pipe of S. Can be done quickly manually, but easier when running both examples and input
    # Looks at neighbours of S and lists which feed into S. From these the sign is chosen. In the 
    # end we overwrite the S value in the input with the correct pipe.
    r, c = s_pos
    s_dirs = set()
    for rr, cc in PRIMARY_AXIS_ADJACENT:
        if not (0 <= r+rr < len(lines) and 0 <= c+cc <= len(lines[0])):
            continue
        if (-rr, -cc) in PIPES[lines[r+rr][c+cc]]:
            s_dirs.add((rr, cc))
    s_pipe = [pipe for pipe, pipe_dirs in PIPES.items() if pipe_dirs == s_dirs][0]
    lines[s_pos[0]] = lines[s_pos[0]].replace('S', s_pipe)
    

    # Find all nodes, only look forward. We know the pipline will never hit a dead end or split.
    nodes = {s_pos}
    new_ends = [s_pos]
    score_p1 = -1
    while new_ends:
        new_ends, ends = [], new_ends
        for r, c in ends:
            char = lines[r][c]
            for rr, cc in PIPES[char]:
                if (r+rr, c+cc) in nodes:
                    continue
                nodes.add((r+rr, c+cc))
                new_ends.append((r+rr, c+cc))
        score_p1 += 1
    
    # Enclosure can be found by looking from anypoint outside the grid and count how ofter you have 
    # crossed a pipe. (I remembered this from determining whether dose voxels are inside a region of
    # interest using DICOM RTDose and RTSS files.)
    # Using I, F 7 works, but I, J, L would work also. The idea is that the inside variable should 
    # flip for a I and a FJ or L7 combination but not a F7 or LJ combination.
    score_p2 = 0
    for r, row in enumerate(lines):
        inside = False
        for c, char in enumerate(row):
            if (r, c) in nodes and char in '|F7':
                inside = not inside
            if inside and not (r, c) in nodes:
                score_p2 += 1

    return (score_p1, score_p2)

if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    input = sys.stdin.read().strip()
    print('  ->', main(input) == (AOC_ANSWER[0], AOC_ANSWER[1]))


