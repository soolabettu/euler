"""Project Euler Problem 719: https://projecteuler.net/problem=719"""

# Tests square numbers for digit partitions whose chunks sum back to the square root.

from functools import lru_cache
from typing import Optional


def can_partition_sum(
    n: int,
    target: Optional[int] = None,
    require_multiple: bool = True,
    allow_leading_zeros: bool = True,
) -> bool:
    """
    Return True iff the decimal digits of n can be split into contiguous parts
    whose integer sum equals `target`. Stops immediately on the first success.

    Pruning:
      - sum of digits > target  => impossible
      - while building a chunk s[i:j], if chunk_value > remaining => break
      - if leading zeros disallowed and chunk has them => break
    """
    s = str(n)
    if target is None:
        target = n

    # Quick lower bound: minimal achievable sum is sum of single digits
    if sum(ord(c) - 48 for c in s) > target:
        return False

    def valid_chunk(i: int, j: int) -> bool:
        # s[i:j] has a leading zero iff s[i] == '0' and length > 1
        return allow_leading_zeros or (j - i == 1 or s[i] != "0")

    @lru_cache(None)
    def dfs(i: int, remaining: int, taken: int) -> bool:
        if i == len(s):
            return remaining == 0 and (not require_multiple or taken >= 2)
        if remaining < 0:
            return False

        val = 0
        for j in range(i + 1, len(s) + 1):
            val = val * 10 + (ord(s[j - 1]) - 48)

            # If this chunk already exceeds remaining, longer chunks will only be larger
            if val > remaining:
                break

            # If leading zeros disallowed and this chunk has one, longer chunks still invalid
            if not valid_chunk(i, j):
                break

            if dfs(j, remaining - val, taken + 1):
                return True  # early exit on first success
        return False

    return dfs(0, target, 0)


# Examples
def solve():
    ans = 0
    limit = 10**12
    for i in range(9, limit + 1):
        if i % 9 > 1:
            continue
        x = i * i
        if x > limit:
            break
        if can_partition_sum(x, target=i, allow_leading_zeros=False):
            ans += x

    return ans


def explore(j, limit, target, digits):
    if j == limit:
        return

    for i in range(j, limit + 1):
        chunk = digits[j, i + 1]
        explore(i + 1, limit)


print(solve())
