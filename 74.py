import mytimeit

from math import gcd, factorial
from fractions import Fraction
from time import sleep
from itertools import permutations


def solve(N):
    """Count numbers below N producing digit factorial chains of length 60."""
    steps = 0
    for i in range(1, N):
        digit_fact_sum = i
        nums = [i]
        while True:
            j = digit_fact_sum
            digit_fact_sum = 0
            while j > 0:
                r = j % 10
                j = j // 10
                digit_fact_sum += factorial(r)

            if digit_fact_sum in nums:
                if len(nums) == 60:
                    print(i)
                    steps += 1
                break

            nums.append(digit_fact_sum)

    return steps


with mytimeit.MyTimer() as t:
    print(solve(1_000_000))
