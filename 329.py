"""Probability propagation for Project Euler problem 329."""

import math
from collections import defaultdict

import mytimeit
from fractions import Fraction
from sympy import isprime


def helper(i, c, prev):
    """Scale probability mass for lily pad `i` based on croak `c`.

    Parameters
    ----------
    i : int
        Zero-based index of the lily pad (pad number is `i + 1`).
    c : str
        Croak character, either ``"P"`` for prime or ``"N"`` for non-prime.
    prev : Fraction
        Incoming probability mass before applying the croak scaling.

    Returns
    -------
    Fraction
        Updated probability mass after applying the croak-specific factor.
    """
    if isprime(i + 1):
        return prev * (Fraction("2/3") if c == "P" else Fraction("1/3"))
    else:
        return prev * (Fraction("1/3") if c == "P" else Fraction("2/3"))


def solve(limit=500):
    """Print the final probability after simulating the frog's croak pattern.

    Parameters
    ----------
    limit : int, optional
        Number of lily pads considered in the simulation, defaults to 500.
    """
    init = [Fraction(f"1/{limit}") for _ in range(limit)]
    pattern = "PPPPNNPPPNPPNPN"
    for i in range(limit):
        init[i] = helper(i, pattern[0], init[i])

    init1 = [Fraction("1/1") for _ in range(limit)]
    pattern = pattern[1:]
    for x in pattern:
        for i in range(limit):
            if i == 0:
                init1[i] = Fraction("1/2") * init[i + 1]
            elif i == limit - 1:
                init1[i] = init[i - 1] * Fraction("1/2")
            elif i == 1:
                init1[i] = init[i - 1] + init[i + 1] * Fraction("1/2")
            elif i == limit - 2:
                init1[i] = init[i - 1] * Fraction("1/2") + init[i + 1]
            else:
                init1[i] = init[i - 1] * Fraction("1/2") + init[i + 1] * Fraction("1/2")

            init1[i] = helper(i, x, init1[i])

        prev = sum(init)
        init = init1.copy()

    print(sum(init))


with mytimeit.MyTimer() as t:
    solve()
