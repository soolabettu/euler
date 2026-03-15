#!/usr/bin/env python
# Advances the Fibonacci sequence until it reaches the first term with 1000 digits.

"""Project Euler Problem 25: https://projecteuler.net/problem=25"""


from datetime import date, timedelta


from collections import defaultdict

sz = 28123
num = []
import sympy

f1 = 1
f2 = 1
sz = 1000000000000000000000000000000000000000000000000
prev = 1
cntr = 2
idx = 2
while True:
    f1, f2 = f2, f1 + f2
    # print(f2)
    # if len(str(f2)) != prev:
    #     print(cntr, f1, f2)
    #     prev = len(str(f2))
    #     cntr = 1
    # else:
    #     cntr += 1
    idx += 1
    if len(str(f2)) >= 1000:
        print(idx)
        break
