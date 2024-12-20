"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
from collections import defaultdict
import itertools as it

AOC_ANSWER = (1507, 1037936)
DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


@print_function
def main(input_txt: str) -> tuple[int, int]:
    """
    Takes advantage of the fact that there is only one possible path (when not cheating). Scans
    through all positions from the S (start). For each newly discovered position we keep track of
    all unvisited path positions within a distance of 20 in the shortcuts dictionary. When we visit
    a place to which shortcuts have already been defined, we check if taking that shortcut saves
    enough time to score (≥ 100 ps).
    """
    # Process input
    grid = input_txt.split('\n')
    unvisited = set()
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            match val:
                case '.' | 'E': 
                    unvisited.add((r, c))
                case 'S':
                    start = (r, c)
    # Find the entire path once.
    r, c = pos = start
    p1, p2 = 0, 0
    shortcuts = defaultdict(dict)
    for path_len in it.count():
        # Scan all positions within 20 steps from the current position
        for dr in range(-20, 21):
            for dc in range(-20+abs(dr), 21-abs(dr)):
                npos = (r + dr, c + dc)
                # If the position is not yet visited, store the distance between the current 
                # position and that position
                if npos in unvisited:
                    shortcuts[npos][pos] = (path_len, abs(dr) + abs(dc))
        # If shortcuts have already been defined to the current position, check how many of them 
        # save > 100 ps.
        for npos, (new_path_len, shortcut_dist) in shortcuts[pos].items():
            time_saved = path_len - new_path_len - shortcut_dist
            if time_saved >= 100:
                if shortcut_dist == 2:
                    p1 += 1
                p2 += 1
        # Look for the unvisited adjacent path
        for dr, dc in DIRS:
            npos = (r + dr, c + dc)
            if npos in unvisited:
                break
        else:
            # No adjacent unvisited position found -> End
            break
        unvisited.remove(npos)
        r, c = pos = npos
    return p1, p2


aoc_run(__name__, __file__, main, AOC_ANSWER)


