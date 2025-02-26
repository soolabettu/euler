#!/usr/bin/env python3

from itertools import permutations

num = "7654321"

import time


def solve():
    import sympy

    for i in permutations(num):
        perm = int("".join(i))
        if sympy.isprime(perm):
            print(perm)
            break


start_time = time.time()
solve()
end_time = time.time()

print("Time taken: %s seconds" % (end_time - start_time))
