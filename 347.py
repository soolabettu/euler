"""Utilities for working with prime factors (Project Euler problem 347 helpers)."""

import math
from collections import defaultdict
from typing import List


def distinct_prime_factors(n: int) -> List[int]:
    """
    Return a sorted list of the distinct prime factors of ``n``.

    The function performs trial division and short-circuits by returning an
    empty list as soon as it detects more than two distinct factors. This is
    useful when callers only care about semiprimes (numbers with at most two
    distinct prime factors).
    """
    if n < 2:
        return []

    factors: List[int] = []

    if n % 2 == 0:
        factors.append(2)
        while n % 2 == 0:
            n //= 2
        if len(factors) > 2:
            return []

    factor = 3
    limit = math.isqrt(n)
    while factor <= limit and n > 1:
        if n % factor == 0:
            factors.append(factor)
            while n % factor == 0:
                n //= factor
            limit = math.isqrt(n)
            if len(factors) > 2:
                return []
        factor += 2

    if n > 1:
        factors.append(n)
        if len(factors) > 2:
            return []

    return factors


def primes_up_to(n: int) -> List[int]:
    """
    Return all prime numbers less than or equal to ``n``.

    Uses a boolean sieve (Sieve of Eratosthenes) and runs in ``O(n log log n)``
    time while using ``O(n)`` memory.
    """
    if n < 2:
        return []

    sieve = [True] * (n + 1)
    sieve[0:2] = [False, False]
    limit = math.isqrt(n)
    for p in range(2, limit + 1):
        if sieve[p]:
            step = p
            start = p * p
            sieve[start : n + 1 : step] = [False] * (((n - start) // step) + 1)

    return [i for i, is_prime in enumerate(sieve) if is_prime]


def is_prime(n: int) -> bool:
    """
    Return ``True`` if ``n`` is prime using a deterministic Miller-Rabin test.

    The implementation first tries division by a small set of primes, then
    executes Miller-Rabin with bases sufficient to guarantee correctness for
    64-bit inputs.
    """
    if n < 2:
        return False

    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    for p in small_primes:
        if n == p:
            return True
        if n % p == 0:
            return n == p

    # write n-1 = d * 2^s
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1

    # Deterministic bases for 64-bit
    bases = [2, 3, 5, 7, 11, 13, 17]
    for a in bases:
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True


def solve(limit=10**7 + 1):
    """
    Compute the sum of maximal semiprime multiples below ``limit``.

    For every unordered pair of primes ``(p, q)`` whose product is below
    ``limit``, the function determines the largest number less than ``limit``
    whose prime factors are exactly ``{p, q}``. Each such maximal product is
    accumulated once.
    """
    my_dict = defaultdict(bool)
    primes = primes_up_to(limit//2)
    for i in range(0, len(primes)):
        for j in range(i + 1, len(primes)):
            if primes[i] * primes[j] > limit:
                break

            ans = max_ab_product_below_N_min1(primes[i], primes[j], limit)
            my_dict[ans[0]] = True

    ans = 0
    for k, v in my_dict.items():
        if v:
            ans += k

    return ans


def max_ab_product_below_N_min1(a: int, b: int, N: int):
    """
    Return the largest product ``a**i * b**j`` strictly below ``N``.

    Parameters
    ----------
    a, b : int
        Base primes (or prime-like integers) with ``a > 1`` and ``b > 1``.
    N : int
        Upper bound that the resulting product must not reach.

    Returns
    -------
    tuple[int, tuple[int, int]]
        The best product along with the exponents ``(i, j)`` that achieve it.
        If no feasible exponents exist (e.g., ``a`` or ``b`` ≤ 1), ``(0, (0, 0))``
        is returned.
    """
    if N <= 1 or a <= 1 or b <= 1:
        # If a<=1 or b<=1, there's no way to have exponent >=1 and increase product meaningfully (<N),
        # and typically no feasible product unless N is huge and the other base helps.
        # We handle properly below by generating powers; this early check is optional.
        pass

    def powers_under_min1(base, limit):
        """Generate (value, exponent) pairs for powers of `base` below `limit`."""
        vals = []
        if base <= 1:
            return vals  # no valid power with exponent >=1
        x, e = base, 1
        while x < limit:
            vals.append((x, e))
            # guard multiply: x * base < limit  <=> x <= (limit - 1) // base
            if x > (limit - 1) // base:
                break
            x *= base
            e += 1
        return vals  # list of (value, exponent), exponents start at 1

    A = powers_under_min1(a, N)
    B = powers_under_min1(b, N)
    if not A or not B:
        return 0, (0, 0)  # no feasible product with i>=1 and j>=1

    # Two-pointer sweep on ascending lists
    best, best_ij = 0, (0, 0)
    j = len(B) - 1
    for ai, ei in A:
        while j >= 0 and ai > (N - 1) // B[j][0]:
            j -= 1
        if j < 0:
            break
        prod = ai * B[j][0]
        if prod > best:
            best = prod
            best_ij = (ei, B[j][1])

    return best, best_ij


import mytimeit





with mytimeit.MyTimer() as t:
    limit = 10**7
    answer = 0
    primes = primes_up_to(limit//2)
    for i in range(1, len(primes)):
        p = primes[i]
        for j in range(i):
            q = primes[j]
            l = limit//q
            if l < p: break
            r = p
            z = []
            while r <= l:
                s = r*q
                while s <= limit: s *= q
                z += [s//q]
                r *= p
            answer += max(z)

    print(answer)

    # print(solve())  # solve()
    # print(max_ab_product_below_N_min1(2, 29, 100))
