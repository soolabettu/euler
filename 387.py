from mytimeit import *
import sympy

visited = set()


def recurse(num: str, limit: int):
    if len(num) > limit:
        return

    n = int(num)

    if len(num) > 1 and sympy.isprime(n):
        prefix = num[:-1]
        n1 = int(prefix)
        s1 = sum(int(c) for c in prefix)
        if s1 and n1 % s1 == 0:
            q = n1 // s1
            if sympy.isprime(q):
                visited.add(n)

    s = sum(int(c) for c in num)
    if s and n % s == 0:
        for d in "0123456789":
            recurse(num + d, limit)


def solve(limit: int):
    for d in "123456789":
        recurse(d, limit)

    print(sum(visited))


with MyTimer() as t:
    solve(14)
