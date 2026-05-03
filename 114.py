from functools import lru_cache


@lru_cache(maxsize=None)
def solve(current_sum, prev_state):
    if current_sum > n:
        return 0

    if current_sum == n:
        return 1

    if prev_state == 0:
        return sum(
            solve(current_sum + length, 1)
            for length in range(3, n - current_sum + 1)
        )

    return sum(
        solve(current_sum + length, 0)
        for length in range(1, n - current_sum + 1)
    )


if __name__ == "__main__":
    n = 50
    print(sum(solve(i, 0) for i in range(n + 1)))
