"""Project Euler Problem 381: https://projecteuler.net/problem=381"""

# Sums the prime-specific factorial remainder expression efficiently over odd primes.

from __future__ import annotations

from math import isqrt


LIMIT = 10**8


def prime_sum(limit: int = LIMIT) -> int:
    if limit < 5:
        return 0

    sieve = bytearray(b"\x01") * ((limit // 2) + 1)
    sieve[0] = 0

    for n in range(3, isqrt(limit) + 1, 2):
        if sieve[n // 2]:
            start = (n * n) // 2
            sieve[start::n] = b"\x00" * (((len(sieve) - start - 1) // n) + 1)

    total = 0
    for p in range(5, limit, 2):
        if sieve[p // 2]:
            total += (-3 * pow(8, -1, p)) % p
    return total


def solve(limit: int = LIMIT) -> int:
    return prime_sum(limit)


if __name__ == "__main__":
    print(solve())
