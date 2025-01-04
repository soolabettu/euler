#!/usr/bin/env python3


import math
import time
from collections import defaultdict
import sympy    


start = time.time()
ans = 0
my_dict = defaultdict(bool)

for i in range(1, 10000):
    if my_dict[i]:
        continue
    
    sum = 1
    for j in range(2, int(math.sqrt(i)) + 1):
        if i % j == 0:
            sum += j + i // j

    sum1 = 1
    for j in range(2, int(math.sqrt(sum)) + 1):
        if sum % j == 0:
            sum1 += j + sum // j

    if sum1 == i and sum != i:
        my_dict[i] = True
        my_dict[sum] = True
        print(sum , i)
        ans += sum + i

print(ans)
end = time.time()
elapsed = end - start
print(f"Program took {elapsed:.2f} seconds to run")