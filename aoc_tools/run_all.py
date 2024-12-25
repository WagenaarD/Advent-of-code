"""
Runs all days from an Advent Of Code year, or all years
python3 ../aoc_tools/run_all.py <YEAR> <ITERATIONS>
pypy3 aoc_tools/run_all.py
"""

import os 
import importlib
import importlib.util
import sys
import datetime
import numpy
import math
from pathlib import Path
from collections import namedtuple

Output = namedtuple('Output', ('day', 'time_s', 'time_sd', 'ans', 'solution'))

def run_year(aoc_year_path: str, repeats: int = 1) -> int:
    aoc_year_path = Path(aoc_year_path)
    year_str = aoc_year_path.parts[-1]
    output = []
    errors = []
    t0 = datetime.datetime.now()
    for day_name in sorted(os.listdir(aoc_year_path)):
        if not day_name.startswith('day_') or day_name.endswith('00'):
            continue
        with open(f'{aoc_year_path}/{day_name}/in') as f:
            input = f.read() # .strip()
        file_path = aoc_year_path / f'{day_name}/main.py'
        mod_name = f'y{file_path.parts[-3]}.{day_name}'
        spec = importlib.util.spec_from_file_location(mod_name, str(file_path))
        code = importlib.util.module_from_spec(spec)
        sys.modules[mod_name] = code
        spec.loader.exec_module(code)
        assert year_str in code.__file__
        time_s = []
        print(f'Starting testing for {year_str}/{day_name}')
        try:
            for _ in range(repeats):
                ans = code.main(input)
                time_s.append((datetime.datetime.now() - t0).total_seconds())
                t0 = datetime.datetime.now()
            time_sd = numpy.std(time_s) / math.sqrt(repeats - 1) if repeats > 1 else None
            output.append(Output(day_name, sum(time_s) / repeats, time_sd, ans, code.AOC_ANSWER))
        except:
            errors.append(f'{day_name} crashed')
    total_time_s = sum([out.time_s for out in output])
    print(f'Speed results {repeats} repeats of all puzzles in {year_str}:')
    for out in output:
        if out.ans == out.solution:
            correct = 'Answer correct'
        else:
            correct = f'INCORRECT, was {out.ans} but was {out.solution}'
        time_pc = out.time_s / total_time_s
        if out.time_sd == None:
            time_sd = ''
            time_pc_sd = ''
        else:
            time_sd = f' ± {out.time_sd:.4f}'
            time_pc_sd = f' ± {out.time_sd / total_time_s:5.1%}'
        print(f' - {out.day} took {out.time_s:.4f}s{time_sd} ({time_pc:5.1%}{time_pc_sd}) - {correct}')
        if out.ans != out.solution:
            errors.append(f'{out.day} took {out.time_s:.4f}s{time_sd} - {correct}')
    print(f'Total time: {total_time_s}s')
    return total_time_s, errors


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    if len(sys.argv) == 3:
        script_path = '/'.join(__file__.replace('\\', '/').split('/')[:-2]) + '/' + sys.argv[1]
        run_year(script_path, int(sys.argv[2]))
    elif len(sys.argv) == 1:
        aoc_path = Path(__file__).parents[1]
        years = [path for path in os.listdir(aoc_path) if path.startswith('20')]
        errors = []
        messages = []
        for year in sorted(years):
            year_time, year_errors = run_year(str(aoc_path / year))
            errors.extend([f'{year}/{mes}' for mes in year_errors])
            messages.append(f'Year {year} completed in {year_time}s')
        if errors:
            print(f'Completed run_all with {len(errors)} errors:\n - ' + '\n - '.join(errors))
        else:
            print('No errors were found')
        print('\n'.join(messages))
    else:
        print(f'Run run_all with two arguments: year and iterations or no arguments')
        print(f'(when ran with no arguments run_all iterates over all years)')
        print(f'{len(sys.argv)-1=}, {sys.argv[1:]=}')