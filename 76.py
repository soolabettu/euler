import mytimeit

from math import gcd, factorial
from fractions import Fraction
from time import sleep
from itertools import permutations


def partitions_dp(n: int) -> int:
    """Number of integer partitions of n (order-insensitive)."""
    dp = [0] * (n + 1)
    dp[0] = 1
    for k in range(1, n + 1):
        for s in range(k, n + 1):
            dp[s] += dp[s - k]
    return dp[n]


# Example
print(partitions_dp(4))  # 5
print(partitions_dp(10))  # 42


def partitions_euler(n: int) -> int:
    """Compute the partition count using Euler's pentagonal number theorem."""
    if n < 0:
        return 0
    p = [0] * (n + 1)
    p[0] = 1
    for m in range(1, n + 1):
        total = 0
        k = 1
        while True:
            g1 = k * (3 * k - 1) // 2
            g2 = k * (3 * k + 1) // 2
            if g1 > m:
                break
            total += (-1) ** (k + 1) * p[m - g1]
            if g2 <= m:
                total += (-1) ** (k + 1) * p[m - g2]
            k += 1
        p[m] = total
    return p[n]


def solve(N):
    """Return the number of partitions of N using Euler's recurrence."""
    return partitions_euler(N)


with mytimeit.MyTimer() as t:
    print(solve(100))
