from __future__ import annotations

"""Project Euler Problem 650: https://projecteuler.net/problem=650

Definitions:
- B(n) = product(C(n, k), k=0..n)
- D(n) = sum of positive divisors of B(n)
- S(N) = sum(D(i), i=1..N) mod MOD

This implementation avoids constructing huge integers and instead works with
prime exponents.
"""

# Builds prime-exponent tables and accumulates the divisor-sum sequence modulo 1e9+7.

MOD = 1_000_000_007


def build_spf(limit: int) -> list[int]:
    """Smallest prime factor table for fast factorizations."""
    spf = list(range(limit + 1))
    if limit >= 1:
        spf[1] = 1
    for i in range(2, int(limit**0.5) + 1):
        if spf[i] == i:
            step = i
            start = i * i
            for j in range(start, limit + 1, step):
                if spf[j] == j:
                    spf[j] = i
    return spf


def factorize_with_spf(x: int, spf: list[int]) -> dict[int, int]:
    """Return prime exponent map for x using precomputed spf."""
    out: dict[int, int] = {}
    while x > 1:
        p = spf[x]
        c = 0
        while x % p == 0:
            x //= p
            c += 1
        out[p] = c
    return out


def solve(n: int) -> int:
    """Return S(n) = sum(D(i), i=1..n) mod MOD."""
    if n <= 0:
        return 0

    spf = build_spf(n)
    primes = [i for i in range(2, n + 1) if spf[i] == i]
    idx_of = {p: i for i, p in enumerate(primes)}
    m = len(primes)

    # a[p] = v_p(k!), where k is current n.
    # f[p] = sum_{i=1..k} v_p(i!).
    a = [0] * m
    f = [0] * m

    # Modular inverses for denominator in sigma(p^e) = (p^(e+1)-1)/(p-1).
    inv_pm1 = [pow(p - 1, MOD - 2, MOD) for p in primes]

    total = 0
    active = 0  # number of primes <= current n

    for k in range(1, n + 1):
        if spf[k] == k and k >= 2:
            active += 1

        for p, v in factorize_with_spf(k, spf).items():
            a[idx_of[p]] += v

        d_k = 1
        kp1 = k + 1
        for i in range(active):
            ai = a[i]
            fi = f[i] + ai
            f[i] = fi
            e = kp1 * ai - 2 * fi
            if e:
                p = primes[i]
                term = (pow(p, e + 1, MOD) - 1) * inv_pm1[i]
                d_k = (d_k * (term % MOD)) % MOD

        total += d_k
        if total >= MOD:
            total -= MOD

    return total


if __name__ == "__main__":

    print(solve(20000))
