"""Project Euler Problem 120: https://projecteuler.net/problem=120"""

# Sums the maximal remainders of (a-1)^n + (a+1)^n modulo a^2 for 3 <= a <= 1000.


def solve():
    """Summation of maximal remainders for the binomial expression problem."""
    return sum(map(lambda a: (a + a % 2 - 2) * a, range(3, 1001)))


print(solve())
