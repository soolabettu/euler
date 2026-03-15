#!/usr/bin/env python3
# Counts integer right triangles by perimeter and returns the busiest perimeter up to 1000.

"""Project Euler Problem 39: https://projecteuler.net/problem=39"""


from collections import defaultdict

my_dict = defaultdict(int)


def solve():
    """Find the perimeter ≤ 1000 yielding the most right triangle solutions."""
    for i in range(1, 1001):
        for j in range(i + 1, 1001):
            if i + j > 1000:
                break
            for k in range(j + 1, 1001):
                if i + j < k:
                    break

                if i + j + k > 1000:
                    continue

                if i * i + j * j == k * k:
                    my_dict[i + j + k] += 1

    print(max(my_dict, key=my_dict.get))


solve()
