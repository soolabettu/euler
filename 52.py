#!/usr/bin/env python3


import math
import time
from collections import defaultdict
import sympy

import resource, sys

resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
sys.setrecursionlimit(10**6)

start = time.time()
i = 1
while True:
    flag = True
    prev = None
    for j in [2, 3, 4, 5, 6]:
        x = i * j
        if prev is not None and prev != sorted(str(x)):
            flag = False
            break

        prev = sorted(str(x))

    if flag:
        print(i)
        break

    i += 1


end = time.time()
elapsed = end - start
print(f"Program took {elapsed:.2f} seconds to run")
