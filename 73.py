import mytimeit

from math import gcd
from fractions import Fraction

#!/usr/bin/env python3
# farey_stream.py
# Stream all reduced proper fractions 0<n<d<=N in ascending order.


def farey_stream(N: int, out_path: str):
    """
    Writes all reduced proper fractions with denominator <= N,
    strictly between 0 and 1, in ascending order, to out_path.
    Each line is 'n/d'.
    """
    # Start with 0/1 and 1/N (first two terms of Farey(N) in [0,1])
    a, b = 0, 1
    c, d = 1, N

    with open(out_path, "w", encoding="utf-8") as f:
        # Iterate until we reach 1/1
        while c <= d and not (c == 1 and d == 1):
            # Write c/d if it's a proper fraction (it always is here except final 1/1)
            if not (c == 0 and d == 1) and not (c == 1 and d == 1):
                f.write(f"{c}/{d}\n")

            # Next term via Farey recurrence:
            # k = floor((N + b) / d); next = (k*c - a) / (k*d - b)
            k = (N + b) // d
            a, b, c, d = c, d, k * c - a, k * d - b


def solve(N):
    farey_stream(N, "reduced_proper_fractions_d_le_12000.txt")


with mytimeit.MyTimer() as t:
    solve(12000)
