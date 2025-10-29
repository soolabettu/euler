def distinct_prime_factors(n):
    """Return sorted list of distinct prime factors of n."""
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
    p = 729809891
    if is_full_reptend_prime_base10(p):
        if last_k_repetend_digits_full_reptend_prime(p, 5) == "56789":
            return (p - 1) * 9 // 2


with mytimeit.MyTimer() as t:
    print(solve())
