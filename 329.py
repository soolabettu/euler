"""Probability propagation for Project Euler problem 329.

The problem describes a frog that begins on an unknown lily pad numbered from
1 to `limit` (inclusive). Each turn the frog croaks, either the letter ``"P"``
or ``"N"`` based on a repeating `pattern`, and then jumps to an adjacent pad.
Pads whose numbers are prime respond differently to the croak than composite
pads, so each croak rescales the probability of the frog occupying a given pad.

This module keeps track of the probability distribution across all pads,
printing the total probability mass after every croak. The final value matches
the answer required by Project Euler 329 when the default parameters are used.
"""

from fractions import Fraction
from typing import Iterable, List

import mytimeit
from sympy import isprime

PASS_FACTOR = Fraction(2, 3)
FAIL_FACTOR = Fraction(1, 3)
HALF = Fraction(1, 2)


def _scale(prob: Fraction, letter: str, is_prime: bool) -> Fraction:
    """Scale a probability mass according to the current croak.

    Parameters
    ----------
    prob
        Probability of the frog currently being on a given lily pad.
    letter
        Single-character croak from the pattern; ``"P"`` means the frog just
        croaked "prime" and ``"N"`` means it croaked "non-prime".
    is_prime
        Whether the lily pad's label (1-based index) is a prime number.

    Returns
    -------
    Fraction
        The corrected probability after applying the croak-specific scaling
        factors laid out in the problem statement.
    """
    if letter == "P":
        return prob * (PASS_FACTOR if is_prime else FAIL_FACTOR)
    return prob * (FAIL_FACTOR if is_prime else PASS_FACTOR)


def _step(probs: Iterable[Fraction]) -> List[Fraction]:
    """Propagate probability mass to neighbouring lily pads.

    The frog moves to one of the two adjacent pads every turn. Interior pads
    receive half of the probability mass from each neighbour, while the two end
    pads only receive half of the probability from their single neighbour.

    Parameters
    ----------
    probs
        An ordered iterable whose entries represent the probability of the frog
        being on each pad after the previous croak.

    Returns
    -------
    list[Fraction]
        The probability distribution after the frog makes its jump.
    """
    probs = list(probs)
    limit = len(probs)
    if limit < 2:
        return probs[:]

    next_probs = [Fraction()] * limit
    next_probs[0] = HALF * probs[1]
    next_probs[-1] = HALF * probs[-2]

    if limit > 2:
        next_probs[1] = probs[0] + HALF * probs[2]
    if limit > 3:
        next_probs[-2] = HALF * probs[-3] + probs[-1]
        for i in range(2, limit - 2):
            next_probs[i] = HALF * (probs[i - 1] + probs[i + 1])

    return next_probs


def solve(limit: int = 500, pattern: str = "PPPPNNPPPNPPNPN") -> None:
    """Print the total probability after each croak in `pattern`.

    Parameters
    ----------
    limit
        Number of pads in the pond. Pads are labelled ``1`` through `limit`
        inclusive; the frog begins on an unknown pad with uniform probability.
    pattern
        The repeating croak sequence. Each character must be ``"P"`` or ``"N"``
        to reflect the statements in the original puzzle.

    Raises
    ------
    ValueError
        If `pattern` is empty, because at least one croak is required to start
        the simulation.

    Side Effects
    ------------
    Prints the sum of the probability distribution after each croak. These
    values allow checking the running totals against the results expected in
    Project Euler 329.
    """
    if not pattern:
        raise ValueError("pattern must contain at least one character")

    primes = [isprime(i) for i in range(1, limit + 1)]
    probs = [_scale(Fraction(1, limit), pattern[0], is_prime) for is_prime in primes]
    print(sum(probs))

    for letter in pattern[1:]:
        probs = _step(probs)
        probs = [
            _scale(prob, letter, is_prime) for prob, is_prime in zip(probs, primes)
        ]
        print(sum(probs))


if __name__ == "__main__":
    with mytimeit.MyTimer():
        solve()
