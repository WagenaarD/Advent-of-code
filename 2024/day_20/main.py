"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run, Tup
from collections import defaultdict
import heapq

AOC_ANSWER = (1507, 1037936)
DIRS = list(map(Tup, [(-1, 0), (0, 1), (1, 0), (0, -1)]))


def dijkstra(start: Tup[int, int], grid: list[str]) -> dict[Tup[int, int], int]:
    """
    Path storing Dijkstra algorithm. Dijkstra algorithm finds the shortest path from a starting 
    state to any other state for positive pathlengths.
    
    Algorithm will quite often need to be tailored before it can be applied. Common changes are:
    - Allow for more complex states, such as the current direction or steps taken
    - Allow for more complex costs between vertices
    """
    qeue = [(0, start)]
    dist = defaultdict(lambda: float('inf'))
    dist[start] = 0
    while qeue:
        cost, pos = heapq.heappop(qeue)
        for dpos in DIRS:
            nr, nc = npos = pos + dpos
            ncost = cost + 1
            if grid[nr][nc] == '#':
                continue
            if ncost < dist[npos]:
                dist[npos] = ncost
                heapq.heappush(qeue, (ncost, npos))
    return dist


@print_function
def part_one(input_txt: str) -> int:
    """
    Calculates how many blocks can be removed to lead to a 100 point time reduction. First calculate
    the distance from start and from end to every position, then look see for any wall in the grid 
    if it as adjacent to a position reached from the start and a position reached from the end. From 
    the distances we can calculate the cheat_time: how long it would take if we force travel through
    this block.

    The code is unnecessarily complex. I did not read that you can assume the path to be a racetrack
    (i.e., there is only one possible path). This could have been used to greatly optimize the code.
    """
    grid = input_txt.split('\n')
    start = [Tup((r, c)) for r, row in enumerate(grid) for c, val in enumerate(row) if val == 'S'][0]
    end = [Tup((r, c)) for r, row in enumerate(grid) for c, val in enumerate(row) if val == 'E'][0]
    dist_from_start = dijkstra(start, grid)
    dist_from_end = dijkstra(end, grid)
    fastest_honest_time = dist_from_start[end]
    p1 = 0
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val != '#':
                continue
            pos = Tup((r, c))
            adj_dists_from_start = (dist_from_start[pos + dpos] for dpos in DIRS)
            adj_dists_from_end = (dist_from_end[pos + dpos] for dpos in DIRS)
            cheat_time = min(adj_dists_from_start) + min(adj_dists_from_end) + 2
            if fastest_honest_time - cheat_time >= 100:
                p1 += 1
    return p1


@print_function
def part_two(input_txt: str) -> int:
    """
    Calculates how cheat paths lead to a 100 point time reduction if we travel through 19 blocks 
    max. First calculate the distance from start and from end to every position, like in part one. 
    Then we look for each position in the from_start path and scan a distance 20 around it. For each
    of these positions we calculate the cheat_time: the time the path would take if we force a path 
    to the first position and exit out of the second position. 

    Again, the code is unnecessarily complex. I did not read that you can assume the path to be a 
    racetrack (i.e., there is only one possible path). This could have been used to greatly optimize 
    the code.
    """
    grid = input_txt.split('\n')
    start = [Tup((r, c)) for r, row in enumerate(grid) for c, val in enumerate(row) if val == 'S'][0]
    end = [Tup((r, c)) for r, row in enumerate(grid) for c, val in enumerate(row) if val == 'E'][0]
    dist_from_start = dijkstra(start, grid)
    dist_from_end = dijkstra(end, grid)
    fastest_honest_time = dist_from_start[end]
    p2 = 0
    for pos in dist_from_start:
        for dr in range(-20, 21):
            for dc in range(-20+abs(dr), 21-abs(dr)):
                cheat_dist = abs(dr) + abs(dc)
                npos = pos + (dr, dc)
                if npos not in dist_from_end:
                    continue
                cheat_time = dist_from_start[pos] + dist_from_end[npos] + cheat_dist
                if fastest_honest_time - cheat_time >= 100:
                    p2 += 1
    return p2


@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        part_one(input_txt), 
        part_two(input_txt)
    )


aoc_run(__name__, __file__, main, AOC_ANSWER)


