"""
A 10 line solution. Possible by not converting to and from ints but staying in SNAFU format.
"""

import sys, collections
SNAFU_DIGIT_LUT = {'2': 2, '1': 1, '0': 0, '-': -1, '=':  -2}
DIGIT_SNAFU_LUT = {val: key for key, val in SNAFU_DIGIT_LUT.items()}
lines = sys.stdin.read().strip().split('\n')
digits = collections.defaultdict(int)
for idx in range(max(len(line) for line in lines)):
    digits[idx] += sum([SNAFU_DIGIT_LUT[line[-idx-1]] for line in lines if len(line) > idx])
    digits[idx + 1] += (digits[idx] - ((digits[idx] + 2) % 5 - 2)) // 5
    digits[idx] = (digits[idx] + 2) % 5 - 2
print(''.join([DIGIT_SNAFU_LUT[digits[idx]] for idx in range(max(digits) + 1)][::-1]).lstrip('0'))