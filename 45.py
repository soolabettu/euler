"""Project Euler Problem 45: https://projecteuler.net/problem=45"""

# Scans triangular numbers until one is also pentagonal and hexagonal.

import math


def solve() -> int:
    """Return the next triangular number that is also pentagonal and hexagonal."""
    n = 286
    while True:
        formula = (n * (n + 1)) / 2
        p = (1 + math.sqrt(1 + 4 * 3 * 2 * formula)) // 6
        h = (1 + math.sqrt(1 + 4 * 2 * formula)) // 4

        f1 = p * (3 * p - 1) / 2
        f2 = h * (2 * h - 1)
        if formula == f1 and formula == f2:
            return formula

        n += 1


print(solve())
