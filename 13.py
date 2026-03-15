#!/usr/bin/env python3
# Sums one hundred large integers from standard input and prints the leading ten digits.

"""Project Euler Problem 13: https://projecteuler.net/problem=13"""


import math

sum = 0
for i in range(100):
    var = input()
    sum += int(var)

print(str(sum)[0:10])
