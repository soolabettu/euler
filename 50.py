#!/usr/bin/env python3

import math
import time
from collections import defaultdict
import sympy

start = time.time()
primes = []
sz = 1000001
for i in range(2, sz + 1):
    if sympy.isprime(i):
        primes.append(i)

sum = 0
cnt = 0
ans = 0
result = 0
for idx, i in enumerate(primes):
    cnt = 1
    sum = i
    for j in range(idx + 1, len(primes)):
        sum += primes[j]
        if sum >= sz:
            break
        cnt += 1
        if sympy.isprime(sum):
            if cnt > ans:
                result = sum
                ans = cnt


print(ans, result)
end = time.time()
elapsed = end - start
print(f"Program took {elapsed:.2f} seconds to run")
