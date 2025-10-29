"""Utilities for Project Euler problem 358 involving full reptend primes."""


def distinct_prime_factors(n):
    """Return the sorted list of distinct prime factors of ``n``.

    Args:
        n (int): Positive integer whose unique prime divisors are needed.

    Returns:
        list[int]: List of the prime divisors of ``n`` ordered increasingly and
        without multiplicity.
    """
    fs = []
    # pull out factors of 2
    if n % 2 == 0:
        fs.append(2)
        while n % 2 == 0:
            n //= 2
    f = 3
    while f * f <= n:
        if n % f == 0:
            fs.append(f)
            while n % f == 0:
                n //= f
        f += 2
    if n > 1:
        fs.append(n)
    return fs


def is_full_reptend_prime_base10(p):
    """Return whether ``p`` is a base-10 full reptend prime.

    Args:
        p (int): Candidate prime to test.

    Returns:
        bool: ``True`` if the decimal expansion of ``1/p`` has maximal period
        ``p - 1`` (i.e. ``p`` is full reptend base 10); otherwise ``False``.
    """
    # quick exclusions
    if p in (2, 5):
        return False
    # assume p is prime; if not sure, primality-test first
    phi = p - 1
    for q in distinct_prime_factors(phi):
        if pow(10, phi // q, p) == 1:
            return False
    return True


def last_k_repetend_digits_full_reptend_prime(p, k=5):
    """Return the final ``k`` digits of the repetend of ``1/p``.

    Args:
        p (int): Full reptend prime in base 10.
        k (int): Number of trailing repetend digits to extract. Defaults to 5.

    Returns:
        str: Concatenated decimal digits (zero-padded as needed) representing
        the last ``k`` digits of the repetend of ``1/p``.
    """
    L = p - 1  # full reptend ⇒ period p-1
    r = pow(10, L - k, p)  # jump to offset L-k
    out = []
    for _ in range(k):
        t = 10 * r
        out.append(t // p)  # next digit
        r = t % p
    return "".join(str(d) for d in out)  # zero-padding intrinsic per digit


# Examples:
# p=7   → '42857'   since 1/7 = 0.\overline{142857}
# p=13  → '76923'   since 1/13 = 0.\overline{076923}
# p=17  → '17647'   since 1/17 = 0.\overline{0588235294117647}


import mytimeit


def solve():
    """Solve Project Euler problem 358.

    Returns:
        int | None: The required value when the candidate prime satisfies the
        problem constraints; ``None`` otherwise.
    """
    p = 729809891
    if is_full_reptend_prime_base10(p):
        if last_k_repetend_digits_full_reptend_prime(p, 5) == "56789":
            return (p - 1) * 9 // 2


with mytimeit.MyTimer() as t:
    print(solve())
