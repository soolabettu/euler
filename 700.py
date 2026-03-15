"""Project Euler Problem 700: https://projecteuler.net/problem=700"""

# Combines forward minima and inverse residues to sum the Eulercoin sequence efficiently.


def solve_eulercoin_fast(print_coins=False):
    a = 1504170715041707
    m = 4503599627370517  # 2^52 + 21

    # Modular inverse: inv * a ≡ 1 (mod m)
    inv = pow(a, -1, m)

    # Phase 1: forward scan with O(1) updates, record running minima
    x = a % m
    cur_min = x
    coins = [x]  # keep only if you want the list
    total = x

    # Tune this cutoff: smaller -> faster forward phase, more inverse work; larger -> opposite.
    # 2_000_000 to 10_000_000 is a good CPython range; PyPy can go larger.
    cutoff = 2_000_000

    while cur_min > cutoff:
        x += a
        if x >= m:
            x -= m
        if x < cur_min:
            cur_min = x
            if print_coins:
                coins.append(x)
            total += x

    # Phase 2: inverse scan over small residues r = 1..cur_min-1
    # r is a new coin iff its earliest index n_r = (inv*r)%m is
    # smaller than any n we've seen so far in this phase.
    best_n = m  # sentinel: larger than any possible n
    r = 1
    while r < cur_min:
        n_r = (inv * r) % m
        if 0 < n_r < best_n:
            best_n = n_r
            if print_coins:
                coins.append(r)
            total += r
        r += 1

    if print_coins:
        # Coins are not necessarily in n-order after phase 2; sort if you need chronological output.
        # Here we just return the set we found.
        return total, coins
    return total


print(solve_eulercoin_fast(print_coins=False))
