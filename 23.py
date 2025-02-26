#!/usr/bin/env python

from datetime import date, timedelta
import time
start = time.time()

from collections import defaultdict
sz = 28123
num = []

import math
for i in range(12, sz + 1):
    temp_sum = 1

    for j in range(2, int(math.sqrt(i)) + 1):
        if i % j == 0:
            temp_sum += j
            x = i//j
            if x != j:
                temp_sum += x

    if temp_sum > i:
        num.append(i)

ans = set()
for idx, i in enumerate(num):
    # print(i)
    for j in range(idx, len(num)):
           if num[idx] + num[j] <= sz:
            ans.add(num[idx] + num[j])


print(28123*28124/2 - sum(ans))
end = time.time()
elapsed = end - start

print(f"Program took {elapsed:.2f} seconds to run")
