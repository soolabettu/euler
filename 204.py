ans = 0
visited = set()

primes_less_than_100 = [
    2,
    3,
    5,
    7,
    11,
    13,
    17,
    19,
    23,
    29,
    31,
    37,
    41,
    43,
    47,
    53,
    59,
    61,
    67,
    71,
    73,
    79,
    83,
    89,
    97,
]


def product(idx, total):

    global ans
    if total in visited or total > 10**9:
        return

    visited.add(total)

    for i in range(idx, len(primes_less_than_100)):
        product(i, total * primes_less_than_100[i])

    return

def solve():
    product(0, 1)
    return len(visited)

from mytimeit import MyTimer

with MyTimer() as t:
    print(solve())
