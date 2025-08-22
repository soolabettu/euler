import mytimeit


def solve():
    return (28433 * (2 ** 7830457) + 1) % (10**10)


with mytimeit.MyTimer() as t:
    print(solve())  # solve()
