def generate_primes(n):
    if n < 2:
        return []

    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False

    limit = int(n**0.5)
    for p in range(2, limit + 1):
        if sieve[p]:
            for multiple in range(p * p, n + 1, p):
                sieve[multiple] = False

    return [num for num in range(2, n + 1) if sieve[num]]


def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    limit = int(n**0.5)
    for factor in range(3, limit + 1, 2):
        if n % factor == 0:
            return False
    return True


def solve():
    primes = generate_primes(10**8)
    ans = set()
    for p in primes:
        r = int(str(p)[::-1])
        s = p * p
        if int(str(s)[::-1]) == s:
            continue
        if is_prime(r):
            t = r * r
            if str(s) == str(t)[::-1]:
                ans.add(s)
                ans.add(t)
                if len(ans) == 50:
                    break

    print(len(ans), sum(ans))


from time import time

if __name__ == "__main__":
    t0 = time()
    solve()
    print(f"Time: {time() - t0:.4f}s")
