"""Project Euler Problem 371: https://projecteuler.net/problem=371"""

# Evaluates the expected-value recurrence for the paired-ticket drawing process.

# https://en.wikipedia.org/wiki/Fibonacci_nim


def solve():
    """Compute expected draw counts for a probabilistic model of paired tickets."""
    M0 = [0] * 500
    M1 = [0] * 500
    M1[499] = 2
    M0[499] = 2 * (1 + M1[499] * 1 / 1000)

    for i in range(498, -1, -1):
        M1[i] = (1000 + ((M1[i + 1] * 2 * (499 - i)))) / (999 - i)
        M0[i] = (1000 + ((M0[i + 1] * 2 * (499 - i))) + M1[i]) / (999 - i)


solve()
