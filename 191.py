def count_valid_iter(n: int) -> int:
    """
    Count strings of length n over {A, O, L} with:
      - no 'AAA' anywhere (<=2 consecutive A's),
      - at most one 'L' total.
    Iterative DP (tabulation) with O(n * 3 * 2) time and O(1) space.
    """
    # dp[runA][usedL]
    dp = [[0, 0], [0, 0], [0, 0]]
    dp[0][0] = 1  # empty prefix

    for _ in range(n):
        new = [[0, 0], [0, 0], [0, 0]]
        for runA in range(3):
            for usedL in (0, 1):
                c = dp[runA][usedL]
                if not c:
                    continue
                # Add 'A' if it won't create 'AAA'
                if runA < 2:
                    new[runA + 1][usedL] += c
                # Add 'L' if we haven't used one yet
                if usedL == 0:
                    new[0][1] += c
                # Add 'O' (always allowed)
                new[0][usedL] += c
        dp = new

    return sum(dp[r][u] for r in range(3) for u in (0, 1))


def solve(limit):
    print(count_valid_iter(limit))


from mytimeit import *

with MyTimer() as t:
    solve(30)
