#!/usr/bin/env python3
# Builds precedence constraints from the login attempts to recover the shortest passcode.

"""Project Euler Problem 79: https://projecteuler.net/problem=79"""


import math
from collections import defaultdict
import sympy

import resource, sys

resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
sys.setrecursionlimit(10**6)


distinct = set()
for i in range(50):
    x = input()
    for v in x:
        distinct.add(int(v))

print(distinct)
