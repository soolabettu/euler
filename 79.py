#!/usr/bin/env python3


import math
import time
from collections import defaultdict
import sympy    

import resource, sys
resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
sys.setrecursionlimit(10**6)

start = time.time()

distinct = set()
for i in range(50):
    x = input()
    for v in x:
        distinct.add(int(v))

print(distinct)

end = time.time()
elapsed = end - start
print(f"Program took {elapsed:.2f} seconds to run")


