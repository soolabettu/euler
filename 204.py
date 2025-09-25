import mytimeit
from sympy import isprime


from math import isqrt

# Example

primes_less_than_100 = [
    2,
    3,
    5,
    7,
    11,
    13,
    17,
    19,
    23,
    29,
    31,
    37,
    41,
    43,
    47,
    53,
    59,
    61,
    67,
    71,
    73,
    79,
    83,
    89,
    97,
]


def divide(n):
    if n == 1:
        return 1

    for p in primes_less_than_100:
        if n % p == 0:
            return divide(n // p)

    return 0


def solve(N):
    cnt = 0
    for i in range(1, N + 1):
        print(i)
        cnt += divide(i)

    return cnt


with mytimeit.MyTimer() as t:
    print(solve(10**9))
