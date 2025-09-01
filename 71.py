import mytimeit

from math import gcd
from fractions import Fraction

#!/usr/bin/env python3
# farey_stream.py
# Stream all reduced proper fractions 0<n<d<=N in ascending order.


from math import floor


def farey_left_neighbor(x, y, a, b, n):
    while y + b <= n:
        x, y = x + a, y + b
    return Fraction(x, y)


def solve(N):
    return farey_left_neighbor(2, 5, 3, 7, N)


with mytimeit.MyTimer() as t:
    print(solve(1000000))
