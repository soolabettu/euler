#!/usr/bin/env python3


import math
import time
from collections import defaultdict
import sympy


start = time.time()
ans = 0
primes = []
for i in range(1000, 10000):
    if sympy.isprime(i):
        primes.append(i)

for i in range(len(primes)):
    for j in range(i + 1, len(primes)):
        if (primes[i] + primes[j]) % 2 == 0:
            k = (primes[i] + primes[j]) // 2
            if (
                k in primes
                and k != primes[i]
                and k != primes[j]
                and sorted(str(primes[i])) == sorted(str(primes[j]))
                and sorted(str(primes[j])) == sorted(str(k))
            ):
                print(primes[i], primes[j], k)

end = time.time()
elapsed = end - start
print(f"Program took {elapsed:.2f} seconds to run")
