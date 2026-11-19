#!/usr/bin/env python3

import math

max_k = 41

# The k = 0 term is exactly 1.
terms = [1.0]
for k in range(1, max_k + 1):
    p = 2.0 ** (-k)
    terms.append(-math.expm1(32 * math.log1p(-p)))

expected_t = math.fsum(terms)
print(f"E[T] ≈ {expected_t:.10f}")
