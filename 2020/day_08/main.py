"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run

AOC_ANSWER = (1394, 1626)


def solve(lines: list[str]) -> int:
    line_idx = 0
    acc_value = 0
    seen = set()
    looped = True
    while line_idx not in seen:
        if line_idx >= len(lines) or line_idx < 0:
            looped = False
            break
        seen.add(line_idx)
        cmd, cmd_var = lines[line_idx].split()
        cmd_var = int(cmd_var)
        if cmd == 'nop':
            line_idx += 1
        elif cmd == 'jmp':
            line_idx += cmd_var
        elif cmd == 'acc':
            acc_value += cmd_var
            line_idx += 1
        else:
            raise(Exception(f'unknown {cmd=} {lines[line_idx]=}'))
    return acc_value, looped


@print_function
def main(input_txt: str) -> tuple[int, int]:
    lines = input_txt.split('\n')
    p1 = solve(lines)[0]
    p2 = None
    for idx, line in enumerate(lines):
        if line[:3] not in ['jmp', 'nop']:
            continue
        new_cmd = {'jmp': 'nop', 'nop': 'jmp'}[line[:3]]
        nlines = lines.copy()
        nlines[idx] = new_cmd + line[3:]
        p2, looped = solve(nlines)
        if not looped:
            break
    return (p1, p2)

aoc_run(__name__, __file__, main, AOC_ANSWER)
