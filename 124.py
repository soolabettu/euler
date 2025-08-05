import mytimeit


import math


def distinct_prime_factors(n: int) -> list[int]:
    """
    Return a list of the distinct prime factors of n, in ascending order.

    >>> distinct_prime_factors(84)   # 84 = 2² · 3 · 7
    [2, 3, 7]
    >>> distinct_prime_factors(97)   # 97 is prime
    [97]
    >>> distinct_prime_factors(1)    # by convention, no prime factors
    []
    """
    if n <= 1:
        return []

    factors = []

    # Handle the factor 2 separately so we can step by 2 later (only odd checks)
    if n % 2 == 0:
        factors.append(2)
        while n % 2 == 0:
            n //= 2

    # Check odd divisors up to √n
    p = 3
    while p * p <= n:
        if n % p == 0:
            factors.append(p)
            while n % p == 0:
                n //= p
        p += 2  # skip even numbers

    # Whatever is left is either 1 or a prime larger than √original n
    if n > 1:
        factors.append(n)

    return factors


import operator
from functools import reduce
from collections import defaultdict

with mytimeit.MyTimer() as t:
    rad = defaultdict(int)
    for i in range(1, 100001):
        factors = distinct_prime_factors(i)
        if factors == []:
            rad[i] = 1
        else:
            rad[i] = reduce(operator.mul, factors, 1)

    ordered_keys = sorted(rad, key=rad.get)
    print(ordered_keys[10000 - 1])
