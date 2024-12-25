"""
Project description here
"""

__project__   = ''
__author__    = 'DW'
__copyright__ = ''
__version__   = '1.0.1'

import sys
from typing import Callable

def aoc_run(name: str, file_path: str, main: Callable, AOC_ANSWER: tuple[int, int], file_name: str = 'in'):
    if name != '__main__':
        return
    if sys.stdin.isatty():
        script_path = '/'.join(file_path.replace('\\', '/').split('/')[:-1])
        with open(f'{script_path}/{file_name}') as f:
            input = f.read().strip()
    else:
        # input = sys.stdin.read().strip()
        input = sys.stdin.read() # Removed .strip() for grid inputs with blank start (2022/day_22)
    print('  ->', main(input) == (AOC_ANSWER[0], AOC_ANSWER[1]))
