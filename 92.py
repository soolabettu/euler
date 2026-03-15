#!/usr/bin/env python3
# Follows square-digit chains and counts how many starting values end at 89.

"""Project Euler Problem 92: https://projecteuler.net/problem=92"""


import math
from collections import defaultdict
import sympy

sz = 10000000


my_dict = defaultdict(set)
cnt = 0
for i in range(1, sz):
    x = i
    sum = 0
    while sum != 89 and sum != 1:
        sum = 0
        while x > 0:
            y = x % 10
            x //= 10
            sum += y * y

        x = sum
        if sum == 89:
            cnt += 1
            # my_dict[89].add(x)
        # elif sum == 1:
        # my_dict[1].add(x)

        # if x in my_dict[89]:
        #     # print(i, x)
        #     cnt += 1
        #     break
        # elif x in my_dict[1]:
        #     break


print(cnt)
