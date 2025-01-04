#!/usr/bin/env python3


import math
import time
from collections import defaultdict
import sympy    


start = time.time()
ans = 0
my_dict = defaultdict(bool)

i = 11
sum = 0
while True:
    var = str(i)
    flag = True
    while var:
        if not sympy.isprime(int(var)):
            flag = False
            break
        var = var[1:]
    

    var = str(i)
    while var:
        if not sympy.isprime(int(var)):
            flag = False
            break
        var = var[:-1]

    if flag:
        print(i)
        sum += i
        ans += 1

    if ans == 11:
        break

    i += 1
    
print(sum)
end = time.time()
elapsed = end - start
print(f"Program took {elapsed:.2f} seconds to run")