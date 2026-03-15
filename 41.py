#!/usr/bin/env python3
# Permutes pandigital digits in descending order and returns the largest prime found.

"""Project Euler Problem 41: https://projecteuler.net/problem=41"""


from itertools import permutations

num = "7654321"


def solve():
    """Return the largest 7-digit pandigital prime."""
    import sympy

    for i in permutations(num):
        perm = int("".join(i))
        if sympy.isprime(perm):
            print(perm)
            break


solve()
