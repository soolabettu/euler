#!/usr/bin/env python3
# Brute-forces Collatz chain lengths below one million to find the longest starting value.

"""Project Euler Problem 14: https://projecteuler.net/problem=14"""


import math

ans = 0
num = 0
for i in range(1, 1000000):
    steps = 0
    x = i
    while x > 1:
        if x % 2 == 0:
            x /= 2
        else:
            x = 3 * x + 1

        steps += 1

    if ans < steps:
        ans = steps
        num = i

print(num)
