#!/usr/bin/env python3
# Extends the number spiral until the diagonal prime ratio falls below ten percent.

"""Project Euler Problem 58: https://projecteuler.net/problem=58"""


from sympy import isprime
import math


def solve():
    """Find the side length where primes on spiral diagonals fall below 10%."""
    x = 2
    num = 1
    cnt = 0
    total_cnt = 1
    ans = 1
    while True:
        for i in range(4):
            num += x
            total_cnt += 1
            if isprime(num):
                cnt += 1

        ans += 1
        x += 2

        # print(cnt, total_cnt, cnt/total_cnt, num)
        # time.sleep(5)
        if cnt / total_cnt < 0.1:
            print(math.sqrt(num))
            break


if __name__ == "__main__":
    solve()
