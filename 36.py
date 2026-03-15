#!/usr/bin/env python3
# Checks integers for palindromicity in both base 10 and base 2.

"""Project Euler Problem 36: https://projecteuler.net/problem=36"""


import math
from collections import defaultdict
import sympy


ans = 0


def is_palindrome(s):
    """Return True if the string s reads the same forwards and backwards."""
    return s == s[::-1]


for i in range(1, 1000000):
    if is_palindrome(str(i)):
        binary_str = bin(i)[2:]
        if is_palindrome(binary_str):
            ans += i


print(ans)
