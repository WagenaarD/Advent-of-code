"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in

Written as an excercise in:
 - DFS as a class wih a recursive function
 - Complex numbers as coordinates
In the end it was equally fast (or slow)
"""
# Start, Part 1, Part 2

AOC_ANSWER = (2386, 6246)

import sys
sys.path.append(AOC_BASE_PATH := '/'.join(__file__.replace('\\', '/').split('/')[:-3]))
from aoc_tools import print_function, aoc_run
from collections import defaultdict, deque
from pprint import pprint

ADJ4 = (-1, 1j, 1, -1j)

DIRS = {
    '.': ADJ4,
    '>': [ 1j],
    '<': [-1j],
    'v': [ 1 ],
    '^': [-1 ],
}

class DFS:
    def __init__(self, grid, nodes, distances, start, end):
        self.nodes: set[complex] = nodes
        # Sorting nodes to explore long paths first. This halved computation time
        for node in distances:
            distances[node] = {k: v for k, v in sorted(distances[node].items(), key=lambda item: item[1], reverse=True)}
        self.distances: dict = distances
        self.max_length: int = sum(char in DIRS for pos, char in grid.items()) - 1
        self.start: complex = start
        self.end: complex = end
        self.seen: set[complex] = {start}
        self.idx: int = 0
        self.ans: int = 0
    
    def run(self, node, dist = 0, missed = 0) -> None:
        self.idx += 1
        # if self.idx % 100_000 == 0: print(f'{self.idx:,}')
        # Paths that are not taken cannot be taken later and are summed as 'missed'. If the total 
        # sum of missed paths is larger than what was missed in the current answer, we do not need
        # to investigate this path further. Improved total paths from 18M to 0.9M and time  from 37s
        # to 5.4s.
        if missed > (self.max_length - self.ans):
            return
        node_distances = sum(nd-1 for other, nd in self.distances[node].items() if not other in self.seen)
        for other in self.distances[node]:
            if other in self.seen:
                continue
            new_missed = missed + node_distances - self.distances[node][other]
            self.seen.add(other)
            self.run(other, dist + self.distances[node][other], new_missed)
            self.seen.remove(other)
        if node == self.end:
            if dist > self.ans:
                self.ans = dist
                return


@print_function
def main(input: str) -> tuple[int, int]:
    # Parse the input
    lines = input.split('\n')
    dims = len(lines), len(lines[0])
    grid = defaultdict(lambda : '#')
    for r, row in enumerate(lines):
        for c, char in enumerate(row):
            grid[complex(r, c)] = char
    start = complex(0, lines[0].find('.'))
    end = complex(dims[1]-1, lines[-1].find('.'))
    # Find all nodes
    nodes = {start, end}
    for pos in grid.keys():
        if grid[pos] in DIRS and pos not in nodes:
            adj = sum([grid[pos + dpos] in DIRS for dpos in ADJ4])
            if adj > 2:
                nodes.add(pos)
    # Calculate distances between nodes without climbing slopes
    distances = defaultdict(dict)
    for node in nodes:
        stack = deque([(node, 0)])
        seen = {node}
        while stack:
            pos, dist = stack.popleft()
            for dpos in DIRS[grid[pos]]:
                npos = pos + dpos
                if npos in seen:
                    continue
                elif npos in nodes:
                    distances[node][npos] = dist + 1 
                elif grid[npos] in DIRS:
                    seen.add(npos)
                    stack.append((npos, dist + 1))
    # If only one node connects to the end, that node MUST go to the end
    # this reduces total paths from 30.5M to 18M (and time from 63s to 37s)
    nodes_leading_into_end = [n for n in nodes if end in distances[n]]
    if len(nodes_leading_into_end) == 1:
        node = nodes_leading_into_end[0]
        distances[node] = {end: distances[node][end]}
    
    # DFS time
    dfs_p1 = DFS(grid, nodes, distances, start, end)
    dfs_p1.run(start)
    for node in nodes:
        for other, dist in distances[node].items():
            if not end in distances[other]:
                distances[other][node] = dist
    dfs_p2 = DFS(grid, nodes, distances, start, end)
    dfs_p2.run(start)
    print(f'{dfs_p1.idx=}, {dfs_p2.idx=}')
    return dfs_p1.ans, dfs_p2.ans


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    if sys.stdin.isatty():
        script_path = '/'.join(__file__.replace('\\', '/').split('/')[:-1])
        with open(f'{script_path}/in') as f:
        # with open(f'{script_path}/ex') as f:
            input = f.read().strip()
    else:
        input = sys.stdin.read().strip()
    print('  ->', main(input) == (AOC_ANSWER[0], AOC_ANSWER[1]))

