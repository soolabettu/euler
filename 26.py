#!/usr/bin/env python

from datetime import date, timedelta
import time
start = time.time()

def fun(d):
    num = 1
    for i in range(d):
        num = (num*10)%d

    num1 = num
    len1 = 0
    while True:
        num = (num*10)%d
        len1 += 1
        if num == num1:
            break
    return d, len1
    

ans = 0
ans_i = 0
for i in range(8, 9):
    num, len1 = fun(i)
    if len1 > ans:
        ans = len1
        ans_i = num

print(ans, ans_i)
end = time.time()
elapsed = end - start
print(f"Program took {elapsed:.2f} seconds to run")
