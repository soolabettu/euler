import mytimeit


def solve():
    modulus = 10000000000
    result = 1
    for t in range(7830457):
        result = (result * 2) % modulus

    return (result * 28433 + 1) % modulus


with mytimeit.MyTimer() as t:
    print(solve())  # solve()
