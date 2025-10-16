# https://projecteuler.net/problem=429

import math


def sieve_of_eratosthenes(limit):
    """Return all primes up to limit inclusive."""
    prime = [True] * (limit + 1)
    p = 2
    while p * p <= limit:
        if prime[p]:
            for i in range(p * p, limit + 1, p):
                prime[i] = False
        p += 1
    return [p for p in range(2, limit + 1) if prime[p]]


def solve(limit):
    """Evaluate the sum of squares of divisors product modulo 1e9+9 up to limit!."""
    upper_limit = int(limit)
    primes = sieve_of_eratosthenes(upper_limit)
    ans = 1
    mod = 10**9 + 9
    for p in primes:
        exp = 1
        base = p
        prime_exp = 0
        while True:
            q = limit // base
            # print(q, base, limit)
            if q == 0:
                break

            exp += 1
            base = p**exp
            prime_exp += q

        # print(p, prime_exp)
        prime_exp *= 2
        total = p
        for i in range(1, prime_exp):
            total = (total * p) % mod
        ans = (ans * (1 + total)) % mod

    return ans


from mytimeit import MyTimer

with MyTimer() as t:
    print(solve(10**8))
