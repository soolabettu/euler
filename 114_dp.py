TARGET_LENGTH = 50
STATE_COUNT = 4

START_RED = 0
MIDDLE_RED = 1
END_RED = 2
BLACK = 3


def solve(length):
    dp = [[0] * STATE_COUNT for _ in range(length + 1)]
    dp[0][BLACK] = 1

    for i in range(1, length + 1):
        previous = dp[i - 1]
        current = dp[i]

        current[START_RED] = previous[BLACK]
        current[MIDDLE_RED] = previous[START_RED]
        current[END_RED] = previous[MIDDLE_RED] + previous[END_RED]
        current[BLACK] = previous[END_RED] + previous[BLACK]

    return dp[length][END_RED] + dp[length][BLACK]


if __name__ == "__main__":
    print(solve(TARGET_LENGTH))
