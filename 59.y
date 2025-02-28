#!/usr/bin/env python3


from itertools import *
from datetime import date, timedelta
import time


import time
import time

from mytimeit import * 


def solve():
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    i = 0
    f = open('./0059_cipher.txt', 'r')
    data = f.read().strip().split(',')
    out = open('output.txt', 'w')
    items = [x for x in alphabet]
    for c in permutations(items, 3):
        out_data = ''
        for item, d in zip(cycle(''.join(c)), data):
            ascii_data = ord(item) ^ int(d)
            t = chr(ascii_data)
            # if not t.islower() and not t.isupper() and t != ' ': 
            #     flag = False
            #     break
            out_data += chr(ascii_data)

        out.write(str(c) + ' ' + out_data)
        out.write('\n')

    out.close()

if __name__ == "__main__":
    with MyTimer(solve) as timer:
        solve()