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
    matrix = [[0 for _ in range(15)] for _ in range(15)]
    for i in range(15):
        matrix[i] = list(map(int, input().split()))

    n = len(matrix)
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
                dp[nm] = max(dp[nm], dp[mask] + matrix[k][j])

    return dp[(1 << n) - 1]


import mytimeit

with mytimeit.MyTimer() as t:
    print(solve())
