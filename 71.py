"""Project Euler Problem 71: https://projecteuler.net/problem=71"""

# Uses Farey-neighbor logic to find the reduced fraction immediately left of 3/7.


from math import gcd
from fractions import Fraction

#!/usr/bin/env python3
# farey_stream.py
# Stream all reduced proper fractions 0<n<d<=N in ascending order.


from math import floor


def farey_left_neighbor(x, y, a, b, n):
    """Return the greatest fraction ≤ n steps left of a/b in Farey sequence of order n."""
    while y + b <= n:
        x, y = x + a, y + b
    return Fraction(x, y)


def solve(N):
    """Find the largest reduced fraction less than 3/7 with denominator up to N."""
    return farey_left_neighbor(2, 5, 3, 7, N)


print(solve(1000000))
