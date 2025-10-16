#!/usr/bin/env python3

from itertools import count

from mytimeit import *
import time
from itertools import *


def solve():
    """Sum pandigital numbers satisfying the substring divisibility property."""
    def find_permutations(s):
        """Return every permutation of the supplied string."""
        return ["".join(p) for p in permutations(s)]

    permutations_list = find_permutations("1406357289")

    divisors = [2, 3, 5, 7, 11, 13, 17]
    ans = 0
    for p in permutations_list:
        flag = True
        my_list = []
        nums = [int(p[i : i + 3]) for i in range(1, len(p) - 2, 1)]
        for x, y in zip(nums, divisors):
            if x % y != 0:
                flag = False
                break

        if flag:
            print(p)
            ans += int(p)

    print(ans)


if __name__ == "__main__":
    with MyTimer(solve) as timer:
        solve()
