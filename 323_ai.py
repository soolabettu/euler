# Computes the exact expected draw count for setting all bits using inclusion-exclusion.

import math
from decimal import Decimal, getcontext


def calculate_exact_expected_value(n):
    # Set precision to 50 digits to ensure the final 10 are perfect
    getcontext().prec = 50

    total_expected = Decimal(0)

    for j in range(1, n + 1):
        # Calculate the components of the term
        # 1. Sign: (-1)^(j+1)
        sign = Decimal(-1) if (j + 1) % 2 else Decimal(1)

        # 2. Binomial Coefficient: n choose j
        # Using math.comb (Python 3.8+) for integer precision
        combination = Decimal(math.comb(n, j))

        # 3. The Fraction: 1 / (1 - 2^-j)
        # Note: 2^-j is 1/(2^j)
        fraction = Decimal(1) / (Decimal(1) - Decimal(2) ** Decimal(-j))

        # Combine them
        term = sign * combination * fraction

        # Add to total
        total_expected += term

    return total_expected


# Example Usage
n = 32
result = calculate_exact_expected_value(n)

# Format to print exactly 10 decimal digits
print(f"Exact result: {result:.10f}")
