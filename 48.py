import mytimeit
import math
import time


def my_pow(x) -> int:
    """Return x^x modulo 10^10 computed iteratively."""
    y = 1
    for i in range(x):
        y = (y * x) % math.pow(10, 10)
    return y


def solve() -> int:
    """Compute the last ten digits of the series sum_{i=1}^{999} i^i."""
    sum = 0
    for i in range(1, 1000):
        sum = sum + my_pow(i) % math.pow(10, 10)
    return str(int(sum))[-10:]


with mytimeit.MyTimer() as t:
    print(solve())
