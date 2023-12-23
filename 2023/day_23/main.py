"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (2386, None)

import sys
sys.path.append(AOC_BASE_PATH := '/'.join(__file__.replace('\\', '/').split('/')[:-3]))
from aoc_tools import print_function
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
    # Calculate all paths from start to end
    stack = deque()
    stack.append((start, 0, [start]))
    paths = []
    # idx = 0
    while stack:
        # if (idx := idx + 1) % 100_000 == 0: print(idx, len(stack))
        node, dist, seen = stack.popleft()
        for other in distances[node]:
            if other in seen:
                continue
            if other not in seen:
                stack.append((other, dist + distances[node][other], seen + [other]))
        if node == end:
            paths.append((dist, seen))
    return max(path[0] for path in paths)
    

@print_function
def main(input: str) -> tuple[int, int]:
    return (solve(input), solve(input, False))


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


