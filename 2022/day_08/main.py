"""
Advent of code challenge 2022
Start  - forgot
Part 1 - forgot - 1700
Part 2 - 20:30  - 470596
"""

import itertools as it

input_lines = open('input.txt').read().split('\n')
tree_height = [[int(char) for char in line] for line in input_lines]

no_rows, no_cols = len(tree_height), len(tree_height[0])
no_visible_trees, max_scenic_score = 0, 0
for row, col in it.product(range(no_rows), range(no_cols)):
    score, visible = 1, False
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        valid = lambda d: 0 <= row + dx * d < no_rows and 0 <= col + dy * d < no_cols
        tree_line = [tree_height[row + dx*d][col + dy*d] for d in it.takewhile(valid, it.count(1))]
        if not any([tree >= tree_height[row][col] for tree in tree_line]):
            visible = True
        for idx, tree in enumerate(tree_line):
            if tree >= tree_height[row][col]:
                score *= (idx + 1)
                break
        else:
            score *= len(tree_line)
    no_visible_trees += visible
    max_scenic_score = max(max_scenic_score, score)

print('Part 1:', no_visible_trees)
print('Part 2:', max_scenic_score)