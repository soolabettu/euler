#!/usr/bin/env python3
# Computes sums of proper divisors and totals the amicable numbers below ten thousand.

"""Project Euler Problem 21: https://projecteuler.net/problem=21"""


import math
from collections import defaultdict
import sympy


ans = 0
my_dict = defaultdict(bool)

for i in range(1, 10000):
    if my_dict[i]:
        continue

    sum = 1
    for j in range(2, int(math.sqrt(i)) + 1):
        if i % j == 0:
            sum += j + i // j

    sum1 = 1
    for j in range(2, int(math.sqrt(sum)) + 1):
        if sum % j == 0:
            sum1 += j + sum // j

    if sum1 == i and sum != i:
        my_dict[i] = True
        my_dict[sum] = True
        print(sum, i)
        ans += sum + i

print(ans)
