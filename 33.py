#!/usr/bin/env python3


def solve():
    """Find digit-canceling fractions among two-digit numerators and denominators."""
    from fractions import Fraction

    two_digit_numbers = [i for i in range(10, 99) if i % 10 != 0]

    for i in two_digit_numbers:
        if i % 10 == i // 10:
            continue

        # Create a Fraction object
        j = i % 10 * 10 + i // 10
        j += 1
        while j // 10 == i % 10:
            f = Fraction(i, j)
            g = Fraction(i // 10, j % 10)
            if f == g:
                print(i, j)
            j += 1


if __name__ == "__main__":
    solve()
