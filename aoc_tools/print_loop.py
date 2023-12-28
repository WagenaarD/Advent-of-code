"""
Project description here
"""

__project__   = ''
__author__    = 'd.wagenaar@umcg.nl'
__copyright__ = 'Copyright UMCG, UMC Groningen - The Netherlands'
__version__   = '1.0.1'

import datetime

PERIOD_IN_SECONDS = 5.0


def print_loop(generator, max_idx = None):
    if max_idx == None:
        max_idx = len(generator)
    generator = iter(generator)
    idx = 0
    t_0 = datetime.datetime.now()
    last_t = t_0
    print(f'Loop: Started ({max_idx} iterations)')
    while True:
        try:
            yield next(generator)
        except StopIteration as err:
            print(f'Loop: Completed')
            return
        idx += 1
        t = datetime.datetime.now()
        if (t - last_t).total_seconds() > PERIOD_IN_SECONDS:
            last_t = t
            print(f'Loop: {idx:5}/{max_idx} eta: {(t - t_0) / idx * (max_idx - idx)}')