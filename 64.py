import mytimeit


import math


def continued_fraction_period(n):
    """
    Calculate the period length of the continued fraction expansion of sqrt(n).
    Returns 0 if n is a perfect square (period would be 0).

    Uses the algorithm for periodic continued fractions of quadratic irrationals.
    """
    # Check if n is a perfect square
    sqrt_n = int(math.sqrt(n))
    if sqrt_n * sqrt_n == n:
        return 0

    # Initialize values for the continued fraction algorithm
    a0 = sqrt_n  # integer part of sqrt(n)
    m = 0
    d = 1
    a = a0

    # Keep track of seen states to detect period
    seen_states = {}
    period_length = 0

    while True:
        # Update m, d, a using the continued fraction recurrence
        m = d * a - m
        d = (n - m * m) // d
        a = (a0 + m) // d

        # Create a state tuple to track when we've seen this combination before
        state = (m, d, a)

        if state in seen_states:
            # We've completed one full period
            break

        seen_states[state] = period_length
        period_length += 1

    return period_length


def find_odd_period_square_roots(limit):
    """
    Find all numbers <= limit whose square roots have odd-length periods
    in their continued fraction expansion.
    """
    odd_period_numbers = []

    for n in range(2, limit + 1):  # Start from 2 since sqrt(1) = 1
        period_len = continued_fraction_period(n)
        if period_len > 0 and period_len % 2 == 1:  # Non-zero and odd
            odd_period_numbers.append((n, period_len))

    return odd_period_numbers


def solve(limit):
    """Count the numbers up to limit whose square roots have odd continued-fraction periods."""
    # print(f"Finding square roots of numbers ≤ {limit} with odd periods...\n")

    odd_period_results = find_odd_period_square_roots(limit)

    # print(f"Found {len(odd_period_results)} numbers whose square roots have odd periods:\n")

    # # Display results in a nice format
    # print("Number | Period Length | √n ≈")
    # print("-" * 35)

    # for n, period in odd_period_results[:50]:  # Show first 50
    #     sqrt_approx = math.sqrt(n)
    #     print(f"{n:6d} | {period:13d} | {sqrt_approx:.6f}")

    # if len(odd_period_results) > 50:
    #     print(f"\n... and {len(odd_period_results) - 50} more numbers")

    return len(odd_period_results)
    # # Some interesting statistics
    # print(f"\nStatistics:")
    # print(f"Total numbers checked: {limit - 1}")
    # print(f"Numbers with odd periods: {len(odd_period_results)}")
    # print(f"Percentage with odd periods: {len(odd_period_results) / (limit - 1) * 100:.2f}%")

    # # Show distribution of period lengths
    # period_counts = {}
    # for _, period in odd_period_results:
    #     period_counts[period] = period_counts.get(period, 0) + 1

    # print(f"\nDistribution of odd period lengths:")
    # for period in sorted(period_counts.keys())[:10]:  # Show first 10 period lengths
    #     count = period_counts[period]
    #     print(f"Period {period}: {count} numbers")


import mytimeit

with mytimeit.MyTimer() as t:
    print(solve(10000))
