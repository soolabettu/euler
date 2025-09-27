is_palindrome = lambda n: str(n) == str(n)[::-1]

visited = set()


def recurse(start, num, total, limit):

    if total >= limit:
        return 0

    if is_palindrome(total) and num - start > 0:
        if total not in visited:
            visited.add(total)

    return recurse(start, num + 1, total + (num + 1) * (num + 1), limit)


def solve(limit):
    for i in range(1, limit):
        recurse(i, i, i * i, limit)

    return sum(visited)


from mytimeit import *

with MyTimer() as t:
    print(solve(10**8))
