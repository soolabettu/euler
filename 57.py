#!/usr/bin/env python3
# Counts sqrt(2) convergents whose numerators have more digits than denominators.

"""Project Euler Problem 57: https://projecteuler.net/problem=57"""


import math
from fractions import Fraction


def solve():
    """Count convergents of sqrt(2) whose numerator has more digits than denominator."""

    f1 = Fraction(2, 1)
    f2 = Fraction(2, 1)
    ans = 0
    for i in range(1000):
        f2 = f1 + 1 / f2
        f3 = 1 + 1 / f2
        ans += len(str(f3.numerator)) > len(str(f3.denominator))

    print(ans)


if __name__ == "__main__":
    solve()
