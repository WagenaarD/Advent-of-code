"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2
# Forgot
# 09:27:24
# 10:12:05

AOC_ANSWER = (506891, 230462)

import sys
sys.path.append('../..')
from aoc_tools import print_function
from collections import defaultdict
import re

def process_label(label: str) -> int:
    value = 0
    for ch in label:
        value = ((value + ord(ch))*17)%256
    return value

@print_function()
def part_one(input: str) -> int:
    return sum([process_label(step) for step in input.split(',')])

@print_function()
def part_two(input: str) -> int:
    lines = input.split(',')
    # Box moving
    boxes = defaultdict(list)
    for line in lines:
        pos = re.search('[-=]', line).start()
        label, operation, focal_length = line[:pos], line[pos], line[pos+1:]
        box_idx = process_label(label)
        same_label = [idx for idx, lens in enumerate(boxes[box_idx]) if lens[0] == label]
        if operation == '=':
            if same_label:
                boxes[box_idx][same_label[0]] = (label, focal_length)
            else:
                boxes[box_idx].append((label, focal_length))
        elif operation == '-':
            if same_label:
                boxes[box_idx].pop(same_label[0])
        # print(f'\nAfter "{line}"')
        # for box_idx, box in boxes.items():
        #     if box:
        #         print(f'Box {box_idx}: ' + ' '.join([f'[{lens[0]} {lens[1]}]' for lens in box]))
    # Scoring
    ans = 0
    for box_idx, box in boxes.items():
        for lens_idx, (label, focal_length) in enumerate(box, 1):
            ans += (box_idx+1) * lens_idx * int(focal_length)
    return ans

@print_function()
def main(input: str) -> tuple[int, int]:
    return(part_one(input), part_two(input))


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    input = sys.stdin.read().strip()
    print('  ->', main(input) == (AOC_ANSWER[0], AOC_ANSWER[1]))


