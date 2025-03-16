import sys

from mytimeit import *


def is_1_to_9_pandigital(num_str):
    """
    Returns True if num_str is exactly 9 characters long and contains
    the digits 1..9 exactly once each. Otherwise False.
    """
    return len(num_str) == 9 and set(num_str) == set("123456789")


def solve():
    f1, f2 = 1, 1  # Starting values as specified
    f3, f4 = 1, 1
    index = 3  # Because we already have f1 (index 1) and f2 (index 2)

    while True:
        # Calculate next Fibonacci number
        f1, f2, f3, f4 = f2, (f1 + f2) % 10**9, f4, (f3 + f4)
        index += 1
        if f4 > 10**9:
            f3 /= 10
            f4 /= 10

        if is_1_to_9_pandigital(str(f2)) and is_1_to_9_pandigital(str(f4)[:9]):
            print(f"Found at index {index}:")
            break


if __name__ == "__main__":

    sys.set_int_max_str_digits(1000000)
    with MyTimer(solve) as timer:
        solve()
