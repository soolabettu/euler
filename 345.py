import math


def solve(n=15):
    """Solve the maximum assignment value for a square matrix from stdin.

    Parameters
    ----------
    n : int, optional
        Dimension of the square matrix to read. Defaults to 15, matching the
        Project Euler 345 specification. The function still infers the exact
        size from the provided input matrix, so this argument is mainly for
        clarity and future tweaks.

    Returns
    -------
    int
        The maximal sum achievable by selecting exactly one element from each
        row and column (i.e., the assignment problem optimum), computed via
        dynamic programming over subsets.
    """
    m = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        m[i] = list(map(int, input().split()))

    @lru_cache(None)
    def dfs(mask, j):
        """Depth-first search over assignment states.

        Parameters
        ----------
        mask : int
            Bitmask representing which rows are still available; bit i set
            indicates row i has not been used yet.
        j : int
            Index of the current column under consideration.

        Returns
        -------
        int
            Maximum attainable sum from assigning columns j..n-1 given the
            remaining available rows encoded in `mask`.
        """
        # base case: all columns assigned
        if j == n:
            return 0

        best = 0
        for i in range(n):
            if mask & (1 << i):  # if row i is available
                new_mask = mask & ~(1 << i)
                best = max(best, m[i][j] + dfs(new_mask, j + 1))

        return best

    # return dfs_iterative(m)
    return dfs((1 << n) - 1, 0)


def dfs_iterative(m):
    """Compute maximum assignment sum using iterative DP over subset masks.

    Parameters
    ----------
    m : list[list[int]]
        Square cost matrix where m[i][j] is the value for picking row i and
        column j together.

    Returns
    -------
    int
        Optimal value of choosing exactly one entry from each row/column,
        evaluated by filling a DP table across partial assignments.
    """
    n = len(m)
    dp = [0] * (1 << n)
    dp[0] = 0

    for k in range(n + 1):
        for mask in range(1 << n):
            if mask.bit_count() != k:
                continue
            # extend with any free task j
            for j in range(n):
                if mask & (1 << j):
                    continue
                nm = mask | (1 << j)
                dp[nm] = max(dp[nm], dp[mask] + m[k][j])

    return dp[(1 << n) - 1]


from functools import lru_cache
import mytimeit

with mytimeit.MyTimer() as t:
    print(solve())
