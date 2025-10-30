"""Solutions for Project Euler problem 88 (minimal product-sum numbers)."""

import math
from collections import defaultdict

import mytimeit

limit = 15


import random
from typing import List, Tuple, Any


def solve(limit=10**12):
    """Accumulate counts of power sums below `limit` and print the final total."""
    total = 0
    my_dict = defaultdict(int)
    x = 2
    flag = True
    while x < limit and flag:
        i = 1
        total = 1
        while total < limit:
            total += pow(x, i)
            if total > limit:
                if i == 2:
                    flag = False
                break

            if total > x + 1:
                my_dict[total] += 1

            i += 1

        x += 1
        print(x)

    ans = 1
    ans += sum([k for k, v in my_dict.items() if v > 0])

    print(ans)


with mytimeit.MyTimer() as t:
    solve()
