#!/usr/bin/env python3
"""Calculate the expected number of distinct colors drawn from an urn."""

import argparse
from decimal import Decimal, getcontext
from math import comb


def expected_distinct_colors(
    draws: int,
    colors: int = 7,
    balls_per_color: int = 10,
) -> Decimal:
    """Return the expected distinct-color count for draws without replacement."""
    total_balls = colors * balls_per_color

    if not 0 <= draws <= total_balls:
        raise ValueError(f"draws must be between 0 and {total_balls}")

    if draws == 0:
        return Decimal(0)

    non_target_balls = total_balls - balls_per_color
    probability_color_absent = (
        Decimal(comb(non_target_balls, draws)) / Decimal(comb(total_balls, draws))
        if draws <= non_target_balls
        else Decimal(0)
    )

    return Decimal(colors) * (Decimal(1) - probability_color_absent)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Expected distinct colors when drawing without replacement."
    )
    parser.add_argument("draws", type=int, nargs="?", default=20)
    parser.add_argument("--colors", type=int, default=7)
    parser.add_argument("--balls-per-color", type=int, default=10)
    parser.add_argument("--precision", type=int, default=9)
    args = parser.parse_args()

    if args.colors <= 0 or args.balls_per_color <= 0:
        parser.error("colors and balls-per-color must be positive")
    if args.precision < 0:
        parser.error("precision must be nonnegative")

    getcontext().prec = max(50, args.precision + 20)

    try:
        result = expected_distinct_colors(
            draws=args.draws,
            colors=args.colors,
            balls_per_color=args.balls_per_color,
        )
    except ValueError as error:
        parser.error(str(error))

    print(f"{result:.{args.precision}f}")


if __name__ == "__main__":
    main()
