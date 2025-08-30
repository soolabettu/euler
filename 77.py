import mytimeit
from math import isqrt


def primes_below(n: int):
    """Return list of all primes < n (sieve of Eratosthenes)."""
    if n <= 2:
        return []
    sieve = bytearray(b"\x01") * n
    sieve[0:2] = b"\x00\x00"  # 0,1 not prime
    for p in range(2, isqrt(n) + 1):
        if sieve[p]:
            step = p
            start = p * p
            sieve[start:n:step] = b"\x00" * ((n - start - 1) // step + 1)
    return [i for i in range(2, n) if sieve[i]]


def count_prime_partitions_below(n: int) -> int:
    """
    Count partitions of n using only primes < n (order-insensitive, duplicates allowed).
    Example: n=10 uses primes {2,3,5,7} and counts:
      (7,3), (5,5), (5,3,2), (3,3,2,2), (2,2,2,2,2)  -> 5
    """
    if n <= 1:
        return 0
    P = primes_below(n)  # primes < n
    if not P:
        return 0

    # Unbounded knapsack / coin-change counting with unique ordering
    dp = [0] * (n + 1)
    dp[0] = 1
    for p in P:
        for s in range(p, n + 1):
            dp[s] += dp[s - p]
    return dp[n]


# Example
def solve(N):
    for i in range(N + 1):
        x = count_prime_partitions_below(i)
        if x >= 5000:
            print(x)
            return i


with mytimeit.MyTimer() as t:
    print(solve(1000))
