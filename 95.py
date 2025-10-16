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


from mytimeit import *

with MyTimer() as t:
    print(solve(1000000))
