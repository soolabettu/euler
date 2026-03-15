"""Project Euler Problem 95: https://projecteuler.net/problem=95"""

# Builds divisor-sum chains and finds the longest amicable cycle below the limit.

import sympy
from collections import defaultdict


import math


# Example usage
def solve(limit):
    """Find the longest amicable chain with members below limit."""
    a = [1] * limit
    for i in range(2, limit):
        for j in range(2 * i, limit, i):
            a[j] += i

    max_chain = []
    for i in range(1, limit):
        num = i
        seen = []
        while num < limit:
            if num in seen:
                if num == i:
                    if len(seen) > len(max_chain):
                        max_chain = seen
                break

            seen.append(num)
            num = a[num]

    return max_chain


print(solve(1000000))
