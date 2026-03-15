"""Project Euler Problem 97: https://projecteuler.net/problem=97"""

# Computes the last ten digits of 28433 * 2^7830457 + 1.


def solve():
    """Return the last ten digits of 28433 * 2^7830457 + 1."""
    return (28433 * (2**7830457) + 1) % (10**10)


print(solve())  # solve()
