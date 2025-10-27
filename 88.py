import math
from collections import defaultdict

import mytimeit


def prime_factors(n):
    """Return the prime factors of ``n`` in non-decreasing order.

    Args:
        n (int): Positive integer whose prime factorisation is required.

    Returns:
        list[int]: Sequence of prime factors. Returns an empty list when
        ``n < 2``.

    Notes:
        Performs trial division by two and then by the odd numbers up to the
        square root of ``n``.
    """
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


def factor_combinations(n):
    """Return all multiplicative partitions of ``n`` excluding the trivial one.

    Args:
        n (int): Integer greater than or equal to two.

    Returns:
        list[tuple[int, ...]]: Sorted list (lexicographically) of tuples where
        each tuple represents a multiset of factors whose product equals ``n``.

    Notes:
        This is a depth-first search over subsets of prime factors. Each tuple
        is normalised (sorted) to avoid duplicate representations.
    """
    primes = prime_factors(n)
    results = set()

    def helper(current, remaining):
        """Depth-first search over combinations of the remaining prime factors."""
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
    """Compute and print the sum of minimal product-sum numbers for ``k`` ≤ 12000."""
    for i in range(2, 24001):
        factors = factor_combinations(i)
        for f in factors:
            s = sum(f)
            p = math.prod(f)
            k = p - s + len(f)
            if k > 12000:
                continue

            my_dict[k].append(p)

        print(i)

    uniq_values = set()
    for k, v in my_dict.items():
        my_dict[k] = sorted(v)

    for k, v in my_dict.items():
        uniq_values.add(v[0])

    print(sum(uniq_values))


with mytimeit.MyTimer() as t:
    solve()
