from functools import lru_cache


def count_valid(n: int) -> int:
    """
    Count strings of length n over {A, O, L} with:
      - no 'AAA' anywhere,
      - at most one 'L' total.
    """

    @lru_cache(None)
    def dp(pos: int, runA: int, usedL: int) -> int:
        if pos == n:
            return 1
        total = 0
        # Place 'A' if it won't create 'AAA'
        if runA < 2:
            total += dp(pos + 1, runA + 1, usedL)
        # Place 'L' if we haven't used any L yet
        if usedL == 0:
            total += dp(pos + 1, 0, 1)
        # Place 'O' (always allowed)
        total += dp(pos + 1, 0, usedL)
        return total

    return dp(0, 0, 0)


if __name__ == "__main__":
    n = 30
    # -> 1918080160


def solve(limit):
    print(count_valid(limit))


from mytimeit import *

with MyTimer() as t:
    solve(30)
