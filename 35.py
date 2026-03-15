#!/usr/bin/env python3
# Tests primes below one million for circular-prime behavior under digit rotation.

"""Project Euler Problem 35: https://projecteuler.net/problem=35"""


import math
from collections import defaultdict
import sympy


primes = defaultdict(bool)

for i in range(2, 1000000):
    if sympy.isprime(i):
        primes[i] = True


def all_rotations(n):
    """Return all cyclic rotations of the decimal representation of n."""
    num_str = str(n)
    rotations = []
    for i in range(len(num_str)):
        rotated_str = num_str[i:] + num_str[:i]
        rotations.append(int(rotated_str))
    return rotations


ans = 0
for k, v in primes.items():
    rotations = all_rotations(k)
    flag = True
    for rotation in rotations:
        if rotation not in primes:
            flag = False
            break

    if flag:
        ans += 1

print(ans)
