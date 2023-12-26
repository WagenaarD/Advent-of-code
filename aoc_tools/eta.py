from datetime import datetime

def eta(idx, t0, max_idx):
    return datetime.strftime((t0 + (datetime.now() - t0) * max_idx / (idx+1)), '%H:%M (%Y-%m-%d)')
