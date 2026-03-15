#!/usr/bin/env python3
# Finds the smallest odd composite that violates Goldbach's other conjecture.

"""Project Euler Problem 46: https://projecteuler.net/problem=46"""


from itertools import permutations

num = "7654321"


def is_perfect_square(n):
    """Return True if n is a perfect square."""
    return (n**0.5).is_integer()


def solve():
    """Find the smallest odd composite that violates Goldbach's other conjecture."""
    import sympy

    i = 1
    num = 5
    while True:
        num += 2
        i = num - 2
        flag = False
        if sympy.isprime(num):
            continue

        while i > 0:
            if sympy.isprime(i) and is_perfect_square((num - i) / 2):
                flag = True
                break
            i -= 2

        if not flag:
            print(num)
            break


solve()
