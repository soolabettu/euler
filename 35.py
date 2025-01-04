#!/usr/bin/env python3


import math
import time
from collections import defaultdict
import sympy    


start = time.time()

primes = defaultdict(bool)

for i in range(2, 1000000):
    if sympy.isprime(i):
        primes[i] = True


def all_rotations(n):
    num_str = str(n)
    rotations = []
    for i in range(len(num_str)):
        rotated_str = num_str[i:] + num_str[:i]
        rotations.append(int(rotated_str))
    return rotations




ans = 0
for k, v in primes.items():
    rotations = all_rotations(k)
    flag = True
    for rotation in rotations:
        if rotation not in primes:
            flag = False
            break

    if flag:
        ans += 1

print(ans)
end = time.time()
elapsed = end - start
print(f"Program took {elapsed:.2f} seconds to run")