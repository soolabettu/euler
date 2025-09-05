
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

def solve(n, limit):
    primes = sieve_primes(limit)
    print(primes)
    updated = [p for p in primes for _ in range(3)]
    permutations = list(itertools.permutations(updated, 3))
    uniq_sums = set()
    # print(permutations)
    for p in permutations:
        result = p[0] ** 2 + p[1] ** 3 + p[2] ** 4
        if result < limit:
            uniq_sums.add(result)
        
    return len(uniq_sums)

    

from mytimeit import *
with MyTimer() as t:
    print(solve(10000, 50_000_000))
