import mytimeit
import math


def complementary_factors(k, n):
    """Return all factor pairs (a, b) such that a*b = n."""
    factors = []
    for i in range(1, k + 1):
        if n % i == 0:
            factors.append((i, n // i))

    return (n, len(factors))


def solve(a018894):
    for i in a018894:
        x, y = complementary_factors(i, i * i)
        # print(x, y)
        if y > 1000:
            return i


import mytimeit

with mytimeit.MyTimer() as t:
    a018894 = [
        1,
        2,
        4,
        6,
        12,
        24,
        30,
        60,
        120,
        180,
        210,
        360,
        420,
        840,
        1260,
        1680,
        2520,
        4620,
        9240,
        13860,
        18480,
        27720,
        55440,
        110880,
        120120,
        180180,
        240240,
        360360,
        720720,
        1441440,
        2162160,
        3603600,
        4084080,
        4324320,
        6126120,
        12252240,
        24504480,
        36756720,
        61261200,
    ]
    print(solve(a018894))
