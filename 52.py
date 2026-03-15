#!/usr/bin/env python3
# Searches for the smallest integer whose first six multiples are digit permutations.

"""Project Euler Problem 52: https://projecteuler.net/problem=52"""


import math
from collections import defaultdict
import sympy

import resource, sys

resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
sys.setrecursionlimit(10**6)

i = 1
while True:
    flag = True
    prev = None
    for j in [2, 3, 4, 5, 6]:
        x = i * j
        if prev is not None and prev != sorted(str(x)):
            flag = False
            break

        prev = sorted(str(x))

    if flag:
        print(i)
        break

    i += 1
