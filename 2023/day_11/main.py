"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2
# 08:02:13
# 08:11:49
# 08:17:22

AOC_ANSWER = (10313550, 611998089572)

import sys
sys.path.append('../..')
from aoc_tools import print_function

@print_function()
def main(input: str, factor: int = 1_000_000) -> 'tuple(int, int)':
    lines = input.split('\n')
    galaxies = [(r, c) for r, row in enumerate(lines) for c, char in enumerate(row) if char == '#']
    # Sum the Manhattan distance between each galaxy pair
    dist = 0
    for idx, (r, c) in enumerate(galaxies):
        for (rr, cc) in galaxies[idx+1:]:
            dist += abs(r-rr) + abs(c-cc)
    # Count the number of times an empty row or column splits a galaxy pair
    empties = 0
    for r, row in enumerate(lines):
        if not '#' in row:
            above = len([1 for (rr, cc) in galaxies if rr < r])
            empties += above * (len(galaxies) - above)
    for c in range(len(lines[0])):
        if not any([line[c] == '#' for line in lines]):
            to_left = len([1 for (rr, cc) in galaxies if cc < c])
            empties += to_left * (len(galaxies) - to_left)        
    # Finish up
    score_p1 = dist + empties
    score_p2 = dist + empties * (factor - 1)
    return (score_p1, score_p2)


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    input = sys.stdin.read().strip()
    if input.count('\n') == 9:
        print('Running for example input')
        print('  ->', main(input, 100) == (374, 8410)) 
    else:   
        print('  ->', main(input) == (AOC_ANSWER[0], AOC_ANSWER[1]))


