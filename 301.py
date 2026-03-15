"""Project Euler Problem 301: https://projecteuler.net/problem=301"""

# Counts n values where n xor 2n xor 3n vanishes, matching the Nim-loss pattern.


def solve(limit=2**30):
    cnt = 0
    for n in range(1, limit + 1):
        x, y, z = n, n * 2, n * 3
        if x ^ y ^ z == 0:
            cnt += 1

    return cnt


print(solve())  # solve()
