
"""
Project Euler 745 scratch implementation.

This file computes

    S(n) = sum_{m=1..n} g(m)

where g(m) is the largest perfect-square divisor of m.

The implementation uses the identity

    count_squarefree(x) = sum_{d^2 <= x} mu(d) * floor(x / d^2)

to count, for each square k^2, how many integers m <= n have largest square
divisor exactly k^2. The contribution of that class is then

    k^2 * count_squarefree(floor(n / k^2)).

This is a direct Möbius-based implementation intended for experimentation and
cross-checking. It is much better than the original brute-force marking
approach, but the nested summation still leaves substantial optimization
headroom for very large n.
"""

from math import isqrt
from time import perf_counter


def generate_mobius(n):
    """Return mu(0..n) using a linear sieve.

    mu(d) is the Möbius function:
    -  1 if d is a product of an even number of distinct primes
    - -1 if d is a product of an odd number of distinct primes
    -  0 if d is divisible by a square

    The squarefree-counting formula in ``solve`` only needs values up to
    floor(sqrt(n)).
    """
    mu = [0] * (n + 1)
    is_prime = [True] * (n + 1)
    primes = []

    mu[1] = 1
    is_prime[0] = is_prime[1] = False

    for i in range(2, n + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1

        for p in primes:
            if i * p > n:
                break
            is_prime[i * p] = False

            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]

    return mu


def solve(n):
    """Compute sum of largest square divisors for 1 <= m <= n, modulo 1e9+7.

    For a fixed k, define the class of numbers

        m = k^2 * s

    where s is squarefree. Exactly those numbers have largest square divisor
    equal to k^2, so the number of such m <= n is the count of squarefree
    integers up to floor(n / k^2).

    The inner loop evaluates that squarefree count with Möbius inversion:

        count_squarefree(x) = sum mu(d) * floor(x / d^2).

    This keeps the logic close to the mathematics, though it still performs a
    nested summation over k and d.
    """
    mod = 10**9 + 7
    root = isqrt(n)
    mu = generate_mobius(root)
    total = 0
    for k in range(1, root + 1):
        d = 1
        cnt = 0
        while True:
            # floor(n / (k^2 * d^2)) is the number of multiples of d^2 that
            # remain after factoring out k^2.
            val = n / ((k * d) ** 2)
            if val < 1:
                break
            cnt += mu[d] * int(val)
            d += 1

        # All numbers whose largest square divisor is exactly k^2 contribute
        # k^2 each to the final sum.
        total = (total + (cnt * (k ** 2)) % mod) % mod
    return total


if __name__ == "__main__":
    # Large input used for performance experiments.
    start = perf_counter()
    n = 10**14
    total = solve(n)
    elapsed = perf_counter() - start
    print(f"Time: {elapsed:.2f} seconds")
    print(f"Total: {total}")
