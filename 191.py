def count_valid_memo(n: int) -> int:
    """
    Count length-n strings over {A,O,L} with:
      - no 'AAA' (≤2 consecutive A's),
      - at most one 'L' in total.
    Recursive + manual memoization (no lru_cache).
    """
    memo = {}  # (pos, runA, usedL) -> count

    def dp(pos: int, runA: int, usedL: int) -> int:
        """Return the number of valid suffixes given the current state."""
        key = (pos, runA, usedL)
        if key in memo:
            return memo[key]
        if pos == n:
            memo[key] = 1
            return 1

        total = 0
        # Place 'A' if it won't make 'AAA'
        if runA < 2:
            total += dp(pos + 1, runA + 1, usedL)
        # Place 'L' if we haven't used any L yet
        if usedL == 0:
            total += dp(pos + 1, 0, 1)
        # Place 'O' (always allowed)
        total += dp(pos + 1, 0, usedL)

        memo[key] = total
        return total

    return dp(0, 0, 0)


# Example:
def solve(limit):
    """Print the number of valid attendance strings of length 30."""
    print(count_valid_memo(30))  # -> 1918080160


from mytimeit import *

with MyTimer() as t:
    solve(30)
