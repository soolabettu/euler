"""Project Euler Problem 99: https://projecteuler.net/problem=99"""

# Compares exponentials by logarithms and returns the line with the largest value.

from math import log10


def solve():
    """Find the 1-indexed line containing the largest exponential value."""
    max_number = 0
    max_line = 0
    with open("0099_base_exp.txt", "r") as f:
        for i, line in enumerate(f):
            base, exp = map(int, line.split(","))
            number = exp * log10(base)
            if number > max_number:
                max_number = number
                max_line = i + 1

    return max_line


print(solve())
