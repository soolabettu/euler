"""Project Euler Problem 918: https://projecteuler.net/problem=918"""

# Evaluates the recursively defined sequence a(n) and prefix sum S(n) by halving recurrences.

from functools import cache
import sys

sys.setrecursionlimit(10000)


def a(n):
    if n < 1:
        raise ValueError("n must be positive")
    if n == 1:
        return 1
    if n % 2 == 0:
        return 2 * a(n // 2)
    else:
        m = (n - 1) // 2
        return a(m) - 3 * a(m + 1)


def S(n):
    if n < 1:
        return 0
    if n == 1:
        return 1
    if n % 2 == 0:
        m = n // 2
        return -S(m) + 4 + S(m - 1)
    else:
        m = (n - 1) // 2
        return S(2 * m) + a(m) - 3 * a(m + 1)


print(S(1000000000000))
