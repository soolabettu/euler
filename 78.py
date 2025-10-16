import mytimeit


def generalized_pentagonals_upto(n):
    """
    Yields generalized pentagonal numbers <= n in the order:
    1, 2, 5, 7, 12, 15, 22, 26, ...
    which corresponds to k = 1, -1, 2, -2, 3, -3, ...
    with P_k = k(3k-1)/2.
    """
    k = 1
    while True:
        for kk in (k, -k):
            g = kk * (3 * kk - 1) // 2
            g %= 10**6
            if g > n:
                return
            yield g
        k += 1


def partitions_upto(N):
    """
    Returns a list p where p[n] = number of partitions of n for 0 <= n <= N.
    Uses Euler's recurrence with signs in pairs: +,+,-,-,+,+,-,-,...
    """
    p = [0] * (N + 1)
    p[0] = 1  # base case

    for n in range(1, N + 1):
        total = 0
        for i, g in enumerate(generalized_pentagonals_upto(n)):
            # sign pattern: +,+,-,-,+,+,-,-,...
            sign = 1 if (i % 4 in (0, 1)) else -1
            total = (total + sign * p[n - g]) % 10**6
        p[n] = total % 10**6
    return p


def p(n):
    """Convenience wrapper: compute a single p(n)."""
    if n < 0:
        return 0
    return partitions_upto(n)[n]


def solve():
    """Find the smallest n such that the partition count p(n) is divisible by one million."""
    N = 100000
    vals = partitions_upto(N)
    for i in range(N + 1):
        if vals[i] % 1000000 == 0:
            print(f"p({i}) = {vals[i]} = {vals[i]/1000000} million")
            break


# --- Demo ---
with mytimeit.MyTimer() as t:
    solve()
