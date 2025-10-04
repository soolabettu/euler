# https://en.wikipedia.org/wiki/Fibonacci_nim

from mytimeit import *


def generate_fibonacci(limit):
    a, b = 1, 1
    fib = [1, 1]
    while a < limit:
        a, b = b, a + b
        fib.append(a)

    return fib


def zeckendorf(orig, n, fibs, idx, prev):
    if n == 0:
        print(orig, prev)
        return prev

    if n < fibs[idx]:
        return zeckendorf(orig, n, fibs, idx + 1, n)

    if n > fibs[idx]:
        return zeckendorf(orig, n - fibs[idx], fibs, idx + 1, n)

    if n == fibs[idx]:
        return zeckendorf(orig, n - fibs[idx], fibs, idx + 1, n)

def solve(limit):
    fib = generate_fibonacci(limit)[2:]
    fib.reverse()
    print(fib)
    ans = 0
    for i in range(1, 101):
        if i in fib:
            continue

        x = fib[0]
        j = 0
        while x > i and j < len(fib):
            j += 1
            x = fib[j]

        y = fib[j]
        if (i - y) * 2 >= y:
            ans += zeckendorf(i, i, fib, 0, 0)           
        else:
            ans = ans + (i - y)

    print(ans)
    return
    A = [0] * (len(fib))
    # Recurence A(Fn) = A(Fn-1) + Fn-2 + A(Fn-2)
    ans = 0
    ans = fib[1] + fib[2]
    for i in range(3, len(fib)):
        A[i] = A[i - 1] + fib[i - 2] + A[i - 2]
        ans += fib[i] + A[i - 1]

    print(ans)


with MyTimer() as t:
    solve(100)
