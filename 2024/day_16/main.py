"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (104516, 545)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run, Tup
import heapq


DIRS = [Tup((-1, 0)), Tup((0, 1)), Tup((1, 0)), Tup((0, -1))]

@print_function
def main(input_txt: str) -> tuple[int, int]:
    """
    Use of Dijkstra algorithm to find the lowest cost to any state in the Reindeer maze. 
    """
    walls = set() # set is 40x quicker than list
    for r, line in enumerate(input_txt.split('\n')):
        for c, char in enumerate(line):
            if char == 'S':
                start = Tup((r, c))
            elif char == 'E':
                end = Tup((r, c))
            elif char == '#':
                walls.add(Tup((r, c)))
    
    # Dijkstra: Create qeue, first item should be cost to minimize
    # For part 1, use Dijkstra's algorithm to calculate the shortest path to any state. A state is 
    # defined as a row, column and direction.
    qeue = [(0, start, DIRS[1])]
    # Dijkstra: Create seen as a dict with the lowest cost to get to stages
    seen = {(start, DIRS[1]): 0}
    # Dijkstra: Start while loop for qeue
    while qeue:
        # Dijkstra: Get the stack item with the lowest score using heappop
        cost, pos, dir = heapq.heappop(qeue)
        seen[(pos, dir)] = cost
        # Dijkstra: Add all new positions
        for ndir in DIRS:
            if dir == ndir:
                npos = pos + dir
                ncost = cost + 1
            elif dir * ndir == (0, 0):
                npos = pos
                ncost = cost + 1000
            else:
                continue
            if (npos, ndir) not in seen and npos not in walls:
                heapq.heappush(qeue, (ncost, npos, ndir))
    # For p1, find the lowest costing value with pos == end
    p1 = min(cost for (pos, dpos), cost in seen.items() if pos == end)

    # For part 2, we reverse look from the end to all states that could be used to reach that state
    qeue = [(cost, pos, dpos) for (pos, dpos), cost in seen.items() if pos == end and cost == p1]
    best_positions = set()
    while qeue:
        cost, pos, dir = qeue.pop()
        best_positions.add(pos)
        # 1: Move one backward
        npos = pos - dir
        if (npos, dir) in seen:
            if seen[(npos, dir)] == cost-1:
                qeue.append((cost-1, npos, dir))
        # 2: Make a turn
        for ndir in DIRS:
            if (dir[0] == 0 and ndir[0] == 0) or (dir[1] == 0 and ndir[1] == 0):
                continue
            if (pos, ndir) in seen and seen[(pos, ndir)] == cost-1000:
                qeue.append((cost-1000, pos, ndir))
    p2 = len(best_positions)

    return p1, p2
        
aoc_run(__name__, __file__, main, AOC_ANSWER)


