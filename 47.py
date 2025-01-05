#!/usr/bin/env python3


import math
import time
from collections import defaultdict
import sympy    

import resource, sys
resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
sys.setrecursionlimit(10**6)

start = time.time()


def fun(num, idx, count):
    if num == 1:
        return distinct_factors
    
    if num % primes[idx] == 0:
        distinct_factors.add(primes[idx])
        count = fun(num // primes[idx], idx, distinct_factors)
    else:
        count = fun(num, idx + 1, count)

    return distinct_factors

ans = 0
primes = []
for i in range(2, 1000000):
    if sympy.isprime(i):
        primes.append(i)

cnt = 0
ans = []
for i in range(2, 1000000):
    distinct_factors = set()
    distinct_factors = fun(i, 0, distinct_factors)
    if len(distinct_factors) == 4:
        ans.append(i)
    else:
        ans = []
    
    if len(ans) == 4:
        print(ans)
        break
        

end = time.time()
elapsed = end - start
print(f"Program took {elapsed:.2f} seconds to run")


