#!/usr/bin/env python3


import math
import time

ans = 0
num = 0
start = time.time()
for i in range(1, 1000000):
    steps = 0
    x = i
    while x > 1:
        if x % 2 == 0:
            x /= 2
        else:
            x = 3 * x + 1

        steps += 1

    if ans < steps:
        ans = steps
        num = i

print(num)
end = time.time()
elapsed = end - start

print(f"Program took {elapsed:.2f} seconds to run")