#!/usr/bin/env python3

from datetime import date, timedelta
import time

start = time.time()

import math

nums = []


def solve():
    x = 10
    ans = 0
    while x < 1000000:
        y = x
        sum = 0
        while y != 0:
            a = y % 10
            y //= 10
            sum += math.factorial(a)
            if sum > x:
                break

        if sum == x:
            nums.append(sum)
            ans += x

        x += 1

    print(ans)


if __name__ == "__main__":
    solve()

end = time.time()
elapsed = end - start

print(f"Program took {elapsed:.2f} seconds to run")
