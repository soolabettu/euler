#!/usr/bin/env python3


import math
import time
from collections import defaultdict
import sympy    


start = time.time()
ans = 0

def is_palindrome(s):
    return s == s[::-1]

for i in range(1, 1000000):
    if is_palindrome(str(i)):
        binary_str = bin(i)[2:]
        if is_palindrome(binary_str):
            ans += i


print(ans)
end = time.time()
elapsed = end - start
print(f"Program took {elapsed:.2f} seconds to run")