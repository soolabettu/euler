import mytimeit
from math import log10
from collections import defaultdict


def prime_factors(n):
    """Return the prime factorization of `n` as a list of factors in non-decreasing order."""
    if n < 2:
        return []

    factors = []
    while n % 2 == 0:
        factors.append(2)
        n //= 2

    factor = 3
    while factor * factor <= n:
        while n % factor == 0:
            factors.append(factor)
            n //= factor
        factor += 2

    if n > 1:
        factors.append(n)

    return factors


import math


def factor_combinations(n):
    primes = prime_factors(n)
    results = set()

    def helper(current, remaining):
        if not remaining:
            results.add(tuple(sorted(current)))
            return

        for i in range(1, 1 << len(remaining)):
            subset = [remaining[j] for j in range(len(remaining)) if (i >> j) & 1]
            product = math.prod(subset)
            if product == 1 or product == n:
                continue
            new_remaining = remaining.copy()
            for x in subset:
                new_remaining.remove(x)
            helper(current + [product], new_remaining)

    helper([], primes)
    return sorted(results)


my_dict = defaultdict(list)


def solve():
    for i in range(2, 24001):
        factors = factor_combinations(i)
        for f in factors:
            s = sum(f)
            p = math.prod(f)
            k = p - s + len(f)
            if k > 12000:
                continue

            my_dict[p - s + len(f)].append(p)

        print(i)

    ans = 0
    uniq_values = set()
    for k, v in my_dict.items():
        my_dict[k] = sorted(v)

    for k, v in my_dict.items():
        uniq_values.add(v[0])

    print(sum(uniq_values))


with mytimeit.MyTimer() as t:
    solve()
