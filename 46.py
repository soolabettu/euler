#!/usr/bin/env python3

from itertools import permutations

num = "7654321"

import time


def is_perfect_square(n):
    return (n**0.5).is_integer()


def solve():
    import sympy

    i = 1
    num = 5
    while True:
        num += 2
        i = num - 2
        flag = False
        if sympy.isprime(num):
            continue

        while i > 0:
            if sympy.isprime(i) and is_perfect_square((num - i) / 2):
                flag = True
                break
            i -= 2

        if not flag:
            print(num)
            break


start_time = time.time()
solve()
end_time = time.time()

print("Time taken: %s seconds" % (end_time - start_time))
