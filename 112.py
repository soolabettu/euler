import mytimeit

from math import gcd
from fractions import Fraction

#!/usr/bin/env python3
# farey_stream.py
# Stream all reduced proper fractions 0<n<d<=N in ascending order.


from math import floor


def solve(N):
    i = 1
    cnt = 0
    while True:
        j = i
        up = True
        down = True
        prev_r = -1
        while j > 0:
            r = j % 10
            j = j // 10
            if prev_r != -1:
                if r < prev_r:
                    down = False
                elif r > prev_r:
                    up = False

            prev_r = r

        if not up and not down:
            cnt += 1

        if cnt / i == 0.99:
            return i

        i += 1


with mytimeit.MyTimer() as t:
    print(solve(10))
