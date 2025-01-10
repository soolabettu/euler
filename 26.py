#!/usr/bin/env python

from datetime import date, timedelta
import time
start = time.time()

def fun(d):
    cnt = 1
    i = 10
    recurring = ''
    r = -1
    print(d)
    times = 5000
    while cnt < times:
        cnt += 1
        while i < d:
            i *= 10
            recurring += '0'
        
        q = i // d
        recurring += str(q)
        r = i % d
        i = r*10
        if len(recurring) % 2 == 0 and len(recurring) > 1:
            if recurring[:len(recurring)//2] == recurring[len(recurring)//2:]:
                # print(recurring)
                return recurring[:len(recurring)//2]

        if r == 0:
            return None
    
    if cnt >= times:
        return None

ans = 0
ans_i = ''
ans_str = ''
for i in range(7, 1000):
    recurring = fun(i)
    if recurring == None:
        continue
    if len(recurring) > ans:
        ans_str = recurring
        ans = len(recurring)
        ans_i = i

print(ans_str*2, ans_i, ans)
end = time.time()
elapsed = end - start
print(f"Program took {elapsed:.2f} seconds to run")
