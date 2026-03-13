"""Project Euler Problem 301: https://projecteuler.net/problem=301"""

from math import factorial


def build_primes(n):
    if n < 2:
        return []

    sieve = [True] * (n + 1)
    sieve[0] = False
    sieve[1] = False

    limit = int(n**0.5)
    for p in range(2, limit + 1):
        if sieve[p]:
            for multiple in range(p * p, n + 1, p):
                sieve[multiple] = False

    return [i for i, is_prime in enumerate(sieve) if is_prime]


def factorial_mod_p_minus_k(p, k):
    # compute (k-1)! mod p
    fact = 1
    for i in range(1, k):
        fact = (fact * i) % p

    # modular inverse of (k-1)!
    inv_fact = pow(fact, -1, p)

    print(inv_fact)

    # (-1)^k mod p
    sign = pow(-1, k, p)

    print(sign)

    print("factorial_mod_p_minus_k:", fact, inv_fact, sign, (sign * inv_fact) % p)
    return (sign * inv_fact) % p


def solve(limit):
    primes = build_primes(limit)
    prime_set = set(primes)
    ans = 0
    total = 0
    for p in primes:
        if p < 5 or p != 7:
            continue

        ans = 0
        for k in range(1, 6):
            print(factorial_mod_p_minus_k(p, k))
            # ans = (ans + factorial_mod_p_minus_k(p, k)) % p

        total += ans

    return total


print(solve(99))  # solve()
