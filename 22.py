#!/usr/bin/env python3


import math
import time
from collections import defaultdict
import sympy

import resource, sys

resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
sys.setrecursionlimit(10**6)

start = time.time()

names = input().split(",")

ans = 0
sorted_names = sorted(names)
for i in range(len(sorted_names)):
    temp = 0
    stripped_word = sorted_names[i].strip('"')
    for j in stripped_word:
        temp += ord(j) - ord("A") + 1

    ans += temp * (i + 1)

print(ans)
end = time.time()
elapsed = end - start
print(f"Program took {elapsed:.2f} seconds to run")
