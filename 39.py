#!/usr/bin/env python3

from collections import defaultdict

my_dict = defaultdict(int)

def solve():
    for i in range(1, 1001):
        for j in range(i+1, 1001):
            for k in range(j+1, 1001):
                    if i + j + k > 1000:
                        continue
                    
                    if i*i + j*j == k*k:
                        my_dict[i + j + k] += 1
                
    print(max(my_dict, key=my_dict.get))


import time

start_time = time.time()

solve()

end_time = time.time()

print("Time taken: %s seconds" % (end_time - start_time))
    