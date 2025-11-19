from collections import defaultdict
from functools import lru_cache

dp = defaultdict(int)
visited = defaultdict(bool)

@lru_cache(maxsize=None)
def solve(state, last):
    global dp, visited



    visited[tuple(state)] = True
    K = sum(i * s for i, s in enumerate(state))

    if K == 0:
        return 0

    ev = 0
    if state[4] != 0:
        new_state = list(state)
        new_state[4] -= 1
        new_state[3] += 1
        if last == 4:
            ev += solve(tuple(new_state), 3) * (4 * (state[4] - 1)) / K
        else:
            ev += solve(tuple(new_state), 3) * (4 * state[4]) / K

    if state[3] != 0:
        new_state = list(state)
        new_state[3] -= 1
        new_state[2] += 1
        if last == 3:
            ev += solve(tuple(new_state), 2) * (3 * (state[3] - 1)) / K
        else:
            ev += solve(tuple(new_state), 2) * (3 * state[3]) / K

    if state[2] != 0:
        new_state = list(state)
        new_state[2] -= 1
        new_state[1] += 1
        if last == 2:
            ev += solve(tuple(new_state), 1) * (2 * (state[2] - 1)) / K
        else:
            ev += solve(tuple(new_state), 1) * (2 * state[2]) / K

    if state[1] != 0:
        new_state = list(state)
        new_state[1] -= 1
        new_state[0] += 1
        if last == 1:
            ev += solve(tuple(new_state), 0) * (1 * (state[1] - 1)) / K
        else:
            ev += solve(tuple(new_state), 0) * (1 * state[1]) / K

    dp[tuple(state)] = 1 + ev
    return 1 + ev

if __name__ == "__main__":
    state = [0, 0, 0, 1, 12]
    print(1 + solve(tuple(state), 3))

