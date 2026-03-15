#!/usr/bin/env python
# Measures recurring cycle lengths of unit fractions and finds the best denominator.

"""Project Euler Problem 26: https://projecteuler.net/problem=26"""


from datetime import date, timedelta


def fun(d):
    """Return the denominator and length of the repeating cycle in 1/d."""
    num = 1
    for i in range(d):
        num = (num * 10) % d

    num1 = num
    len1 = 0
    while True:
        num = (num * 10) % d
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
