import mytimeit


import math


def continued_fraction_period(n):
    """Return the sum of digits of the numerator of the nth convergent of e."""
    p2, p1, q2, q1, a = 0, 1, 1, 0, 2

    k = 1
    x = 1
    for i in range(n):
        p1, p2, q1, q2 = a * p1 + p2, p1, a * q1 + q2, q1
        # print(p1, q1)
        if k % 3 == 1:
            a = 1
        elif k % 3 == 2:
            a = 2 * x
            x += 1
        else:
            a = 1

        k += 1

    return sum([int(c) for c in str(p1)])


def solve(n):
    """Compute the requested digit sum for the nth convergent of e."""
    return continued_fraction_period(n)


import mytimeit

with mytimeit.MyTimer() as t:
    print(solve(100))
