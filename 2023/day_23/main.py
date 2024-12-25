"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (2386, 6246)

import sys
sys.path.append(AOC_BASE_PATH := '/'.join(__file__.replace('\\', '/').split('/')[:-3]))
from aoc_tools import print_function, aoc_run
from collections import defaultdict, deque


DIRS = {
    True: {
        '.': ((-1, 0), (1, 0), (0, -1), (0, 1)),
        '>': (( 0,  1),),
        '<': (( 0, -1),),
        'v': (( 1,  0),),
        '^': ((-1,  0),),
    },
    False: {
        key: ((-1, 0), (1, 0), (0, -1), (0, 1)) for key in '.><v^'
    },
}


def visualize(grid, nodes):
    for r, row in enumerate(grid):
        out = ''
        for c, char in enumerate(row):
            if (r, c) in nodes:
                out += '█'
            else:
                out += char
        print(out)


def solve(input: str, slopes = True) -> int:
    grid = input.split('\n')
    start = [(0, c) for c, char in enumerate(grid[0]) if char == '.'][0]
    end = [(len(grid)-1, c) for c, char in enumerate(grid[-1]) if char == '.'][0]
    # Find all nodes
    nodes = {start, end}
    for r, row in enumerate(grid):
        for c, char in enumerate(row):
            if char in DIRS[slopes] and r in range(1, len(grid)-1) and c in range(1, len(grid[0]) - 1):
                if sum([grid[r+dr][c+dc] in DIRS[slopes] for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1))]) >= 3:
                    nodes.add((r, c))
    # visualize(grid, nodes)
    # Make a dict with the distances between all nodes
    distances = defaultdict(dict)
    for node in nodes:
        stack = deque([(*node, 0)])
        seen = {node}
        while stack:
            r, c, dist = stack.popleft()
            if not (r in range(0, len(grid)) and c in range(0, len(grid[0]))):
                continue
            for dr, dc in DIRS[slopes][grid[r][c]]:
                rr = r + dr
                cc = c + dc
                if not (rr in range(0, len(grid)) and cc in range(0, len(grid[0]))):
                    continue 
                if (rr, cc) in seen:
                    continue
                elif (rr, cc) in nodes:
                    distances[node][(rr, cc)] = dist + 1 
                elif grid[rr][cc] in DIRS[slopes]:
                    seen.add((rr, cc))
                    stack.append((rr, cc, dist + 1))
    # If only one node connects to the end, that node MUST go to the end
    # this reduces total paths from 30.5M to 18M (and time from 63s to 37s)
    nodes_leading_into_end = [n for n in nodes if end in distances[n]]
    if len(nodes_leading_into_end) == 1:
        node = nodes_leading_into_end[0]
        distances[node] = {end: distances[node][end]}
    # Calculate all paths from start to end
    max_length = sum(input.count(char) for char in '.<>v^') - 1
    stack = deque([(start, 0, [start], 0)])
    ans = 0
    idx = 0
    # seen = {key: key == start for key in nodes}
    while stack:
        idx += 1
        if idx % 100_000 == 0: print(f'{idx:,}')
        node, dist, seen, missed = stack.pop()
        # Paths that are not taken cannot be taken later and are summed as 'missed'. If the total 
        # sum of missed paths is larger than what was missed in the current answer, we do not need
        # to investigate this path further. Improved total paths from 18M to 0.9M and time  from 37s
        # to 5.4s.
        if missed > (max_length - ans):
            continue
        node_distances = sum(nd-1 for other, nd in distances[node].items() if not other in seen)
        for other in distances[node]:
            if other in seen:
                continue
            new_missed = missed + node_distances - distances[node][other]
            stack.append((other, dist + distances[node][other], seen + [other], new_missed))
        if node == end:
            if dist > ans:
                ans = dist
    print(f'{idx=:,}')
    return ans
    

@print_function
def main(input: str) -> tuple[int, int]:
    return (solve(input), solve(input, False))

aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')
# aoc_run(__name__, __file__, main, AOC_ANSWER, 'ex')