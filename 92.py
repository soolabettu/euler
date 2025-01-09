#!/usr/bin/env python3

import math
import time
from collections import defaultdict
import sympy    

start = time.time()
sz = 10000000

import time

my_dict = defaultdict(set)
cnt = 0
for i in range(1, sz):
    x = i
    sum = 0
    while sum != 89 and sum != 1:
        sum = 0
        while x > 0:
            y = x%10
            x //= 10
            sum += y * y
        
        x = sum
        if sum == 89: 
            cnt += 1
            # my_dict[89].add(x)
        # elif sum == 1:
            # my_dict[1].add(x)

        # if x in my_dict[89]:
        #     # print(i, x)
        #     cnt += 1
        #     break
        # elif x in my_dict[1]:
        #     break


        

print(cnt)

end = time.time()
elapsed = end - start
print(f"Program took {elapsed:.2f} seconds to run")


