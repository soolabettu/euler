import mytimeit


def sqrt_long_division(n: int, digits: int) -> str:
    """
    Compute sqrt(n) to `digits` decimal places using the digit-by-digit (long division) method.
    Returns a string representation.
    """
    # scale n so we can extract digits after decimal
    n_scaled = n * (100**digits)  # equivalent to (n * 10^(2*digits))

    # digit-by-digit square root extraction
    root = 0
    remainder = 0

    # process pairs of digits (long division style)
    pairs = str(n_scaled)
    if len(pairs) % 2 == 1:  # make even length
        pairs = "0" + pairs

    # split into digit pairs
    pairs = [int(pairs[i : i + 2]) for i in range(0, len(pairs), 2)]

    for p in pairs:
        remainder = remainder * 100 + p
        x = 0
        while (20 * root + (x + 1)) * (x + 1) <= remainder:
            x += 1
        remainder -= (20 * root + x) * x
        root = root * 10 + x

    # now root is sqrt(n * 10^(2*digits))
    s = str(root)
    return sum([int(i) for i in s])


# Example
def solve(N):
    """Return the sum of digital sums for square roots of non-perfect squares up to N."""
    ans = 0
    perfect_squares = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
    for i in range(1, N + 1):
        if i in perfect_squares:
            continue
        ans += sqrt_long_division(i, 99)

    return ans


with mytimeit.MyTimer() as t:
    print(solve(100))
