"""
Taken from reddit
https://www.reddit.com/r/adventofcode/comments/zmcn64/2022_day_15_solutions/jbprd3y/?context=8&depth=9

     __
  __|_A|__
 |_D|_S|_B|
    |_C|
     
"""



import re, sys
def all_numbers(s): return [int(d) for d in re.findall("(-?\d+)", s)]
def md(p, q): return abs(p[0]-q[0])+abs(p[1]-q[1])

input_data = sys.stdin.read().strip()# Added for data processing
data = [all_numbers(line) for line in input_data.split("\n")]
radius = {(a,b):md((a,b),(c,d)) for (a,b,c,d) in data}
scanners = radius.keys()


acoeffs, bcoeffs = set(), set()
for ((x,y), r) in radius.items():
    acoeffs.add(y-x+r+1)
    acoeffs.add(y-x-r-1)
    bcoeffs.add(x+y+r+1)
    bcoeffs.add(x+y-r-1)

bound = 4_000_000
for a in acoeffs:
    for b in bcoeffs:
        p = ((b-a)//2, (a+b)//2)
        if all(0<c<bound for c in p):
            if all(md(p,t)>radius[t] for t in scanners):
                print('(a, b)', (a, b))
                print('(x, y)', p) # ADDED

                print(4_000_000*p[0]+p[1])