"""
Runs all days from an Advent Of Code year
"""

import os, importlib, sys, datetime, numpy, math
from collections import namedtuple
Output = namedtuple('Output', ('day', 'time_s', 'time_sd', 'ans', 'solution'))


def run_all(aoc_year_path: str = '../2023', repeats: int = 1, plot: bool = False) -> int:
    output = []
    sys.path.insert(0, aoc_year_path)
    t0 = datetime.datetime.now()
    for day_name in sorted(os.listdir(aoc_year_path)):
        if not day_name.startswith('day_') or day_name.endswith('00'):
            continue
        with open(f'{aoc_year_path}/{day_name}/in') as f:
            input = f.read().strip()
        code = importlib.import_module(f'{day_name}.main')
        time_s = []
        print(f'Starting testing for {day_name}')
        for _ in range(repeats):
            ans = code.main(input)
            time_s.append((datetime.datetime.now() - t0).total_seconds())
            t0 = datetime.datetime.now()
        time_sd = numpy.std(time_s) / math.sqrt(repeats - 1) if repeats > 1 else None
        output.append(Output(day_name, sum(time_s) / repeats, time_sd, ans, code.AOC_ANSWER))
    total_time_s = sum([out.time_s for out in output])
    print(f'Speed results {repeats} repeats of all puzzles in {aoc_year_path}:')
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
    print(f'Total time: {total_time_s}s')
    if plot:
        try:
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots()
            labels = [out.day[4:] for out in output]
            values = [out.time_s for out in output]
            # bar_labels = ['red', 'blue', '_red', 'orange']
            bar_colors = ['tab:blue'] * len(output)
            ax.bar(labels, values, color=bar_colors)
            ax.set_ylabel('Run time [s]')
            year = aoc_year_path.split('/')[-1]
            ax.set_title(f'AOC {year} results ')
            # ax.legend(title='Fruit color')
            plt.show()
        except ImportError: # Not in pypy3
            pass
    
    return total_time_s


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    script_path = '/'.join(__file__.replace('\\', '/').split('/')[:-2]) + '/' + sys.argv[1]
    run_all(script_path, int(sys.argv[2]), sys.argv[3].lower() == 'y')