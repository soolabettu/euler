# https://en.wikipedia.org/wiki/Fibonacci_nim

from mytimeit import *
from functools import lru_cache

@lru_cache(None)
def is_losing(n, limit):
    """Return True when the current player loses with heap size n and max take limit."""
    if n <= limit:
        return False

    for i in range(1, limit+1):
        if is_losing(n - i, 2*i):
            return False

    return True


def generate_fibonacci(limit):
    """Generate Fibonacci numbers up to the first term >= limit."""
    a, b = 1, 1
    fib = [1, 1]
    while a < limit:
        a, b = b, a + b
        fib.append(a)

    return fib


def zeckendorf(orig, n, fibs, idx, prev):
    """Compute Zeckendorf decomposition trace for orig and echo intermediate states."""
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
    """Explore Fibonacci Nim positions up to limit and accumulate winning moves."""
    fib = generate_fibonacci(limit)[2:]
    print(fib)
    return
    fib.reverse()
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
    max_val = 0
    n = 18
    ans = 0
    prev = 0
    for n in range(1, 610):
        valid_moves = [i for i in range(1, n) if is_losing(n - i, 2 * i)]
        if valid_moves:
            #print(n, max(valid_moves))
            ans = (ans + max(valid_moves)) % 10**8
            if n == 100:
                print(ans)
        else:
            print(ans)
            #print(prev, ans, ans - prev)
            prev = ans
            #ans = 0
        
    print(ans)
