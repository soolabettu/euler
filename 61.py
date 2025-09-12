from mytimeit import *


def polygonal_number(s, n):
    """Return the nth s-gonal number."""
    return n * ((s - 2) * n - (s - 4)) // 2


def four_digit_polygonals():
    """Generate 4-digit numbers for s=3..8 (triangle..octagon)."""
    result = {s: [] for s in range(3, 9)}

    for s in range(3, 9):
        n = 1
        while True:
            p = polygonal_number(s, n)
            if p > 9999:
                break
            if p >= 1000:
                result[s].append(p)
            n += 1
    return result


# Example usage

from time import sleep


def find_next(poly_nums, num_type, idx, last_two_digits, ans):
    if idx == len(num_type):
        q = ans[0]
        r = q % 10
        q //= 10
        r = q % 10
        q //= 10
        r = q % 10
        q //= 10

        x = q % 10 * 10 + r
        r = ans[-1] % 10
        q = ans[-1] // 10
        q %= 10
        y = q % 10 * 10 + r

        if x == y:
            print(sum(ans))

        return

    for i in poly_nums[num_type[idx]]:
        q = i
        r = q % 10
        q //= 10
        r = q % 10
        q //= 10
        r = q % 10
        q //= 10
        if q == last_two_digits // 10 and r == last_two_digits % 10:
            r = i % 10
            q = i // 10
            find_next(poly_nums, num_type, idx + 1, q % 10 * 10 + r, ans + [i])

    return


from itertools import permutations


# Example usage
def solve():
    poly_nums = four_digit_polygonals()
    for permutation in permutations([3, 4, 5, 6, 7, 8]):
        # print(permutation)
        for i in poly_nums[permutation[0]]:
            r = i % 10
            q = i // 10
            q %= 10
            last_two_digits = q * 10 + r
            find_next(poly_nums, permutation, 1, last_two_digits, [i])

    return


with MyTimer() as t:
    print(solve())
