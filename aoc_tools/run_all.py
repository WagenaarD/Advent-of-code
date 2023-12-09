"""
Runs all days from an Advent Of Code year
"""

import os, importlib, sys, datetime
from collections import namedtuple
Output = namedtuple('Output', ('day', 'time_s', 'ans', 'solution'))


def run_all(aoc_year_path = '../2023'):
    output = []
    sys.path.insert(0, aoc_year_path)
    t0 = datetime.datetime.now()
    for day_name in sorted(os.listdir(aoc_year_path)):
        if not day_name.startswith('day_') or day_name.endswith('0'):
            continue
        with open(f'{aoc_year_path}/{day_name}/in') as f:
            input = f.read().strip()
        code = importlib.import_module(f'{day_name}.main')
        ans = code.main(input)
        t0, time_s = datetime.datetime.now(), (datetime.datetime.now() - t0).total_seconds()
        output.append(Output(day_name, time_s, ans, code.AOC_ANSWER))
    total_time_s = sum([out.time_s for out in output])
    print(f'Test results for {aoc_year_path}:')
    for out in output:
        if out.ans == out.solution:
            correct = 'Answer correct'
        else:
            correct = f'INCORRECT, was {out.ans} but was {out.solution}'
        time_pc = out.time_s / total_time_s
        print(f' - {out.day} took {out.time_s:.3f}s ({time_pc:5.1%}) - {correct}')
    print(f'Total time: {total_time_s}s')


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    script_path = '/'.join(__file__.replace('\\', '/').split('/')[:-2]) + '/' + sys.argv[1]
    run_all(script_path)