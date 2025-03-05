#!/usr/bin/env python3

from itertools import count

from mytimeit import *
import time


def solve():
    def agen():
        for k in count(1):
            yield from list(map(int, str(k)))

    a = agen()
    ans = 1
    for i in range(10000001):
        x = next(a)
        if i + 1 in [1, 10, 100, 1000, 10000, 100000, 1000000]:
            ans *= x

    print(ans)


if __name__ == "__main__":
    with MyTimer(solve) as timer:
        solve()
