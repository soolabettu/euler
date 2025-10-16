import mytimeit

from math import gcd
from fractions import Fraction

#!/usr/bin/env python3
# farey_stream.py
# Stream all reduced proper fractions 0<n<d<=N in ascending order.


def totients_up_to(N: int):
    """phi[i] = φ(i) for i=0..N via classic sieve (O(N log log N))."""
    phi = list(range(N + 1))
    for p in range(2, N + 1):
        if phi[p] == p:  # p is prime
            for k in range(p, N + 1, p):
                phi[k] -= phi[k] // p
    return phi


def reduced_proper_fraction_count(N: int) -> int:
    """Return the number of reduced proper fractions with denominator up to N."""
    phi = totients_up_to(N)
    return sum(phi[1:]) - 1  # subtract 0/1


def solve(N):
    """Print the count of reduced proper fractions with denominator up to N."""
    print(reduced_proper_fraction_count(N))


with mytimeit.MyTimer() as t:
    solve(1_000_000)
