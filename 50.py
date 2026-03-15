#!/usr/bin/env python3
# Finds the prime below one million that is the longest sum of consecutive primes.

"""Project Euler Problem 50: https://projecteuler.net/problem=50"""


import math
from collections import defaultdict
import sympy

primes = []
sz = 1000001
for i in range(2, sz + 1):
    if sympy.isprime(i):
        primes.append(i)

sum = 0
cnt = 0
ans = 0
result = 0
for idx, i in enumerate(primes):
    cnt = 1
    sum = i
    for j in range(idx + 1, len(primes)):
        sum += primes[j]
        if sum >= sz:
            break
        cnt += 1
        if sympy.isprime(sum):
            if cnt > ans:
                result = sum
                ans = cnt


print(ans, result)
