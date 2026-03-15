"""Project Euler Problem 692: https://projecteuler.net/problem=692"""

# Uses Fibonacci-Nim recurrences to accumulate the required game-state total.

# https://en.wikipedia.org/wiki/Fibonacci_nim


def generate_fibonacci(limit):
    """Return Fibonacci numbers up to limit inclusive."""
    a, b = 1, 1
    fib = [1, 1]
    while a < limit:
        a, b = b, a + b
        fib.append(a)

    return fib


def solve(limit):
    """Compute the cumulative sum used in the Fibonacci Nim analysis up to limit."""
    fib = [0] + generate_fibonacci(limit)[2:]
    A = [0] * (len(fib))
    # Recurence A(Fn) = A(Fn-1) + Fn-2 + A(Fn-2)
    ans = 0
    ans = fib[1] + fib[2]
    for i in range(3, len(fib)):
        A[i] = A[i - 1] + fib[i - 2] + A[i - 2]
        ans += fib[i] + A[i - 1]

    print(ans)


solve(23416728348467685)
