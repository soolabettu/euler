#!/usr/bin/env python
# Brute-forces quadratic coefficients and tracks the longest consecutive prime run.

"""Project Euler Problem 27: https://projecteuler.net/problem=27"""


from datetime import date, timedelta


import sympy

primes = []
for i in range(2, 1001):
    if sympy.isprime(i):
        primes.append(i)


ans = 0
x = 0
y = 0
for i in primes:
    for j in range(1, 1000, 2):
        expr = 0
        n = 0
        while True:
            expr = n * n + j * n + i
            if sympy.isprime(expr):
                if n > ans:
                    prod = j * i
                    ans = n
                    x, y = j, i
            else:
                break

            n += 1

    for j in range(1, 1000, 2):
        expr = 0
        n = 0
        while True:
            expr = n * n - j * n + i
            if expr < 0:
                break
            if sympy.isprime(expr):
                if n > ans:
                    prod = -j * i
                    ans = n
                    x, y = j, i
            else:
                break
            n += 1

print(prod, ans, x, y)
