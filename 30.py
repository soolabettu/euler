#!/usr/bin/env python3

from itertools import count

from mytimeit import *
import time


def solve():
    """Sum numbers that can be written as the sum of fifth powers of their digits."""
    import math

    ans = 0
    for i in range(10, 1000000):
        x = i
        sum = 0
        while x != 0:
            rem = x % 10
            x //= 10
            sum += math.pow(rem, 5)

        if sum == i:
            ans += sum

    print(ans)


if __name__ == "__main__":
    with MyTimer(solve) as timer:
        solve()
