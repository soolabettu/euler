import math
from collections import defaultdict

import mytimeit


def prime_factors(n):
    """Return the prime factorization of ``n`` as a list of prime factors.

    Args:
        n (int): Target integer to factorise.

    Returns:
        list[int]: Prime factors of ``n`` in non-decreasing order. Returns an
        empty list when ``n`` < 2.
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


def extend_factorizations(factorizations, p):
    """Return all factorizations after integrating a prime factor ``p``.

    Args:
        factorizations (Iterable[tuple[int, ...]]): Existing multiplicative
            partitions represented as sorted tuples.
        p (int): Prime factor to incorporate.

    Returns:
        set[tuple[int, ...]]: New set containing all extended factorizations.
    """
    result = set()
    for f in factorizations:
        f = tuple(sorted(f))
        # append p as a new factor
        result.add(tuple(sorted(f + (p,))))
        # multiply one element by p
        for i in range(len(f)):
            new = list(f)
            new[i] *= p
            result.add(tuple(sorted(new)))
    return result


def prime_factorization(n: int):
    """Return the unique prime factorisation of ``n``.

    Args:
        n (int): Positive integer to factor.

    Returns:
        list[tuple[int, int]]: Sequence of ``(prime, exponent)`` pairs ordered
        by the prime.
    """
    f = []
    x = n
    d = 2
    while d * d <= x:
        if x % d == 0:
            e = 0
            while x % d == 0:
                x //= d
                e += 1
            f.append((d, e))
        d = 3 if d == 2 else d + 2  # 2, then odds
    if x > 1:
        f.append((x, 1))
    return f


def extend_by_prime(factorizations, p):
    """Return factorizations after distributing prime ``p``.

    Args:
        factorizations (Iterable[tuple[int, ...]]): Multiplicative partitions
            stored as sorted tuples.
        p (int): Prime factor to distribute.

    Returns:
        set[tuple[int, ...]]: Deduplicated set of sorted tuples representing
        every way ``p`` can extend the input factorizations.
    """
    out = set()
    for t in factorizations:
        if not t:
            # empty → only option is to start with (p,)
            out.add((p,))
            continue
        # option 1: append p
        out.add(tuple(sorted(t + (p,))))
        # option 2: merge p into any existing factor
        for i in range(len(t)):
            new_t = list(t)
            new_t[i] *= p
            out.add(tuple(sorted(new_t)))
    return out


def multiplicative_partitions(n: int):
    """Return all non-trivial multiplicative partitions of ``n``.

    Args:
        n (int): Integer ≥ 2 whose unordered factorizations are needed.

    Returns:
        list[tuple[int, ...]]: Sorted list of unique factorizations where each
        tuple is in non-decreasing order and omits the trivial factorization
        ``(n,)``.
    """
    if n <= 1:
        return []

    pf = prime_factorization(n)
    # Start from the empty factorization
    S = {()}  # set of tuples

    for p, e in pf:
        for _ in range(e):
            S = extend_by_prime(S, p)

    # Remove trivial (n,) if present
    S.discard((n,))
    # Sort for nice output (by length, then lexicographically)
    return sorted(S, key=lambda t: (len(t), t))


def solve():
    """Solve Project Euler problem 88.

    Builds multiplicative partitions for every integer up to 24 000, tracks the
    minimal product-sum numbers for set sizes up to 12 000, and prints the sum
    of the unique minimal values.
    """
    limit_k, limit_n = 12000, 24000
    my = defaultdict(list)

    for n in range(2, limit_n + 1):
        for f in multiplicative_partitions(n):
            if (k := (p := math.prod(f)) - (s := sum(f)) + len(f)) <= limit_k:
                my[k].append(p)

    uniq_values = {min(v) for v in my.values()}
    print(sum(uniq_values))


with mytimeit.MyTimer() as t:
    solve()
