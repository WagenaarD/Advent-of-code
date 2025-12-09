"""
"""

__project__   = ''
__author__    = 'Dirk'
__copyright__ = ''
__version__   = '1.0.1'

import datetime
try:
    import connect
    RAYSTATION = True
except:
    RAYSTATION = False


def print_loop(generator, max_idx = None, period_in_seconds: float = 5.0):
    """
    Call over an iterator to print messages every five seconds with a time estimate how long the 
    rest of the loop will take. If the supplied generator does not have __len__ implemented, a 
    max_idx needs to be supplied.
    Example:

    for idx in print_loop(range(100)):
        do_stuff()
    >> Loop: Started 100 iterations
    >> Loop: 13/100, time remaining 0:33.126741
    >> Loop: 27/100, time remaining 0:26.834614
    >> Loop: 41/100, time remaining 0:21.213151
    >> Loop: 53/100, time remaining 0:16.981641
    >> Loop: 69/100, time remaining 0:11.872461
    >> Loop: 84/100, time remaining 0:06.813741
    >> Loop: 97/100, time remaining 0:01.814751
    >> Loop: Completed
    """
    if max_idx == None:
        max_idx = len(generator)
    generator = iter(generator)
    idx = 0
    t_0 = datetime.datetime.now()
    last_t = t_0
    print(f'Loop: Started ({max_idx} iterations)')
    while True:
        t = datetime.datetime.now()
        try:
            yield next(generator)
        except StopIteration as err:
            print(f'Loop: Completed in {t-t_0}')
            return
        idx += 1
        message = f'Loop: {idx:5}/{max_idx}, time remaining: {(t - t_0) / idx * (max_idx - idx)}'
        if RAYSTATION:
            connect.set_progress(message, idx/max_idx*100.0)
        if (t - last_t).total_seconds() > period_in_seconds:
            last_t = t
            print(message)