"""
Advent of code challenge 2022
Start  17:37
Part 1 17:39 - 1480
Part 2 17:44 - 2746
Clean  17:48 
"""


def find_distinct_substring(input: str, length: int) -> int:
    for idx in range(len(input)):
        if len(set(input[idx:idx+length])) == length:
            return idx + length


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    input = open('input.txt').read()
    print('Part 1:', find_distinct_substring(input, 4))
    print('Part 2:', find_distinct_substring(input, 14))
