"""Project Euler Problem 63: https://projecteuler.net/problem=63"""

# Counts positive integers that are both n-digit numbers and exact nth powers.

from math import isqrt


# Example
def solve():
    """Count n-digit positive integers that are also nth powers."""
    ans = set([1])
    i = 2
    flag = True
    while True:
        j = 1
        running_total = 0
        while True:
            x = i**j
            if len(str(x)) == j:
                ans.add(x)
            else:
                if j == 1:
                    flag = False
                break

            j += 1

        if not flag:
            break

        i += 1

    return len(ans)


print(solve())
