#!/usr/bin/env python3
# Searches for primes that remain prime under both left and right truncation.

"""Project Euler Problem 37: https://projecteuler.net/problem=37"""


import math
from collections import defaultdict
import sympy


ans = 0
my_dict = defaultdict(bool)

i = 11
sum = 0
while True:
    var = str(i)
    flag = True
    while var:
        if not sympy.isprime(int(var)):
            flag = False
            break
        var = var[1:]

    var = str(i)
    while var:
        if not sympy.isprime(int(var)):
            flag = False
            break
        var = var[:-1]

    if flag:
        print(i)
        sum += i
        ans += 1

    if ans == 11:
        break

    i += 1

print(sum)
