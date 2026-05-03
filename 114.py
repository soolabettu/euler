from functools import lru_cache

cache = {}


def solve(current_sum, prev_state):
    if (prev_state, current_sum) in cache:
        return cache[(prev_state, current_sum)]

    if current_sum > n:
        return 0
    if current_sum == n:
        return 1

    total = 0
    if prev_state == 0:
        for length in range(3, n - current_sum + 1):
            total += solve(current_sum + length, 1)
    else:
        for length in range(1, n - current_sum + 1):
            total += solve(current_sum + length, 0)

    cache[(prev_state, current_sum)] = total
    return total


if __name__ == "__main__":
    n = 50
    total = 0
    for i in range(n + 1):
        total += solve(i, 0)
    print(total)
