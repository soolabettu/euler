#!/usr/bin/env python3


import math

seq = 1
i = 2
while True:
    seq = seq + i
    i = i + 1
    count = 0
    for j in range(1, int(math.sqrt(seq)) + 1):
        if seq % j == 0:
            count += 2

    if count > 500:
        print(seq)
        break
