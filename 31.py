#!/usr/bin/env python3
# Uses coin-change dynamic programming to count ways to make 200 pence.

"""Project Euler Problem 31: https://projecteuler.net/problem=31"""


def solve():
    """Count combinations of UK coins that sum to two pounds."""
    dp = [[0] * 201]
    for i in range(1, 8):
        dp.append([0] * (201))

    dp[0][0] = 1
    w = [1, 2, 5, 10, 20, 50, 100, 200]
    for i in range(8):
        for j in range(201):
            dp[i][j] += dp[i - 1][j]
            if j >= w[i - 1]:
                dp[i][j] += dp[i][j - w[i - 1]]

    print(dp[7][200])


if __name__ == "__main__":
    solve()
