#!/usr/bin/env python3
"""Compute or grid-search success probabilities for Project Euler problem 267."""

from __future__ import annotations

import argparse
from decimal import Decimal, ROUND_HALF_UP, localcontext
from fractions import Fraction
from math import comb


TOSSES = 1_000
TARGET_WEALTH = Fraction(1_000_000_000)


def success_probability(f: Fraction) -> Fraction:
    """Return the exact probability of reaching the target for the chosen f."""
    win_multiplier = 1 + 2 * f
    loss_multiplier = 1 - f

    # When f == 1, any loss reduces the wealth to zero.
    if loss_multiplier == 0:
        successful_outcomes = int(win_multiplier**TOSSES >= TARGET_WEALTH)
        return Fraction(successful_outcomes, 2**TOSSES)

    # Start with the wealth for zero wins, then replace one loss with one win
    # at each step. Fractions keep the target comparison exact.
    wealth = loss_multiplier**TOSSES
    win_for_loss = win_multiplier / loss_multiplier
    minimum_wins: int | None = None

    for wins in range(TOSSES + 1):
        if wealth >= TARGET_WEALTH:
            minimum_wins = wins
            break
        wealth *= win_for_loss

    if minimum_wins is None:
        return Fraction(0)

    successful_sequences = sum(
        comb(TOSSES, wins) for wins in range(minimum_wins, TOSSES + 1)
    )
    return Fraction(successful_sequences, 2**TOSSES)


def format_probability(probability: Fraction, digits: int) -> str:
    """Format an exact probability rounded to the requested decimal places."""
    with localcontext() as context:
        context.prec = max(50, digits + 20)
        value = Decimal(probability.numerator) / Decimal(probability.denominator)
        quantum = Decimal(1).scaleb(-digits)
        return str(value.quantize(quantum, rounding=ROUND_HALF_UP))


def search_hundredths() -> tuple[list[int], Fraction]:
    """Find the best f values among 0.00, 0.01, ..., 1.00."""
    best_hundredths: list[int] = []
    best_probability = Fraction(-1)

    for hundredths in range(101):
        probability = success_probability(Fraction(hundredths, 100))

        if probability > best_probability:
            best_probability = probability
            best_hundredths = [hundredths]
        elif probability == best_probability:
            best_hundredths.append(hundredths)

    return best_hundredths, best_probability


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Calculate the probability of having at least one billion pounds "
            "after 1,000 flips. If f is omitted, search all proportions from "
            "0.00 through 1.00 in increments of 0.01."
        )
    )
    parser.add_argument(
        "f",
        nargs="?",
        type=Fraction,
        help=(
            "optional fixed betting proportion from 0 to 1 "
            "(for example: 0.25 or 1/4)"
        ),
    )
    parser.add_argument(
        "--digits",
        type=int,
        default=12,
        help="number of digits after the decimal point (default: 12)",
    )
    args = parser.parse_args()

    if args.f is not None and not 0 <= args.f <= 1:
        parser.error("f must be between 0 and 1, inclusive")
    if args.digits < 0:
        parser.error("--digits must be nonnegative")

    return args


def main() -> None:
    args = parse_arguments()

    if args.f is not None:
        probability = success_probability(args.f)
        print(format_probability(probability, args.digits))
        return

    best_hundredths, best_probability = search_hundredths()
    formatted_values = ", ".join(
        f"{hundredths // 100}.{hundredths % 100:02d}"
        for hundredths in best_hundredths
    )
    print(f"Best f value(s): {formatted_values}")
    print(f"Probability: {format_probability(best_probability, args.digits)}")


if __name__ == "__main__":
    main()
