#!/usr/bin/env python
# Marks abundant numbers and sums integers that cannot be written as two abundant numbers.

"""Project Euler Problem 23: https://projecteuler.net/problem=23"""


from datetime import date, timedelta


from collections import defaultdict

sz = 28123
num = []

import math

for i in range(12, sz + 1):
    temp_sum = 1

    for j in range(2, int(math.sqrt(i)) + 1):
        if i % j == 0:
            temp_sum += j
            x = i // j
            if x != j:
                temp_sum += x

    if temp_sum > i:
        num.append(i)

ans = set()
for idx, i in enumerate(num):
    # print(i)
    for j in range(idx, len(num)):
        if num[idx] + num[j] <= sz:
            ans.add(num[idx] + num[j])


print(28123 * 28124 / 2 - sum(ans))
