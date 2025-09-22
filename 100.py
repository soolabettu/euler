from math import isqrt
from typing import List, Tuple, Optional

import math


def generate_pairs_pell(n_max: int) -> List[Tuple[int, int, int, int]]:
    """
    Generate all solutions to 2*n(n+1) = m(m+1) with 1 <= n <= n_max
    using the Pell equation v^2 - 2u^2 = -1 with:
        u = 2n + 1, v = 2m + 1
    This produces only valid pairs and is extremely fast.
    """
    out = []
    v, u = 1, 1  # corresponds to n = m = 0 (degenerate; we'll skip)
    while True:
        # (v + u√2) ← (v + u√2) * (3 + 2√2)
        v, u = 3 * v + 4 * u, 2 * v + 3 * u
        n, m = (u - 1) // 2, (v - 1) // 2
        if n > n_max:
            break
        if n >= 1:
            a = n * (n + 1)
            b = m * (m + 1)
            out.append((n, m, a, b))
    return out


def solve(limit):
    return generate_pairs_pell(10**12)


pell_pairs = solve(10**25)
for p in pell_pairs:
    if p[1] + 1 > 10**12:
        print(p[0] + 1)
        break
