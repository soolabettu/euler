def sieve_primes(limit: int) -> list[int]:
    """Return a list of primes up to and including limit using Sieve of Eratosthenes."""
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False  # 0 and 1 are not primes

    p = 2
    while p * p <= limit:
        if sieve[p]:
            # Mark all multiples of p as not prime
            for multiple in range(p * p, limit + 1, p):
                sieve[multiple] = False
        p += 1

    return [i for i, is_prime in enumerate(sieve) if is_prime and i * i <= limit]


import itertools


def solve(limit):
    primes = sieve_primes(limit)
    bucket1 = [prime**2 for prime in primes if prime**2 < 50_000_000]
    bucket2 = [prime**3 for prime in primes if prime**3 < 50_000_000]
    bucket3 = [prime**4 for prime in primes if prime**4 < 50_000_000]
    uniq_sums = set()
    for b1 in bucket1:
        for b2 in bucket2:
            for b3 in bucket3:
                x = b1 + b2 + b3
                if x < limit:
                    uniq_sums.add(x)

    return len(uniq_sums)


from mytimeit import *

with MyTimer() as t:
    print(solve(50_000_000))
