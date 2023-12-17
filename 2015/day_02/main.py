"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (1586300, 3737498)

import sys
sys.path.append('../..')
from aoc_tools import print_function
import re


def part_one(input: str) -> int:
    lines = input.split('\n')
    ans = 0
    for line in lines:
        nums = sorted([int(num) for num in re.findall('\d+', line)])
        ans += 2 * (nums[0] * nums[1] + nums[0] * nums[2] + nums[1] * nums[2])
        ans += nums[0] * nums[1]
    return ans


def part_two(input: str) -> int:
    lines = input.split('\n')
    ans = 0
    for line in lines:
        nums = sorted([int(num) for num in re.findall('\d+', line)])
        ans += 2 * (nums[0] + nums[1])
        ans += nums[0] * nums[1] * nums[2]
    return ans


@print_function()
def main(input: str) -> tuple[int, int]:
    return (part_one(input), part_two(input))


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    input = sys.stdin.read().strip()
    print('  ->', main(input) == (AOC_ANSWER[0], AOC_ANSWER[1]))


