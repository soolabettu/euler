import sympy
from collections import defaultdict

visited = defaultdict(bool)

smallest_sum = float("inf")
smallest_lst = None


def sieve_primes(limit: int) -> list[int]:
    """Return a list of primes up to and including limit using Sieve of Eratosthenes."""
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False  # 0 and 1 are not primes

    p = 2
    while p * p <= limit:
        if sieve[p]:
            # Mark all multiples of p as not prime
            for multiple in range(p * p, limit + 1, p):
                sieve[multiple] = False
        p += 1

    return [i for i, is_prime in enumerate(sieve) if is_prime and i > 2]


from itertools import permutations


def concat_two(nums):
    """Return True if every concatenation of ordered pairs in nums yields a prime."""
    for a, b in permutations(nums, 2):  # ordered pairs
        x = int(str(a) + str(b))
        if visited[x] or not sympy.isprime(x):
            return False

        if not sympy.isprime(x) and not visited[x]:
            visited[x] = True

    return True


def prime_pair_sets(idx, running_lst, primes):
    """Recursively search for sets of five primes with the concatenation property."""
    global smallest_sum, smallest_lst

    if len(running_lst) == 5:
        if sum(running_lst) < smallest_sum:
            smallest_sum = sum(running_lst)
            smallest_lst = running_lst

        print(f"Smallest so far {smallest_lst} -> {smallest_sum}")
        return

    if idx == len(primes):
        return

    for i in range(idx, len(primes)):
        if concat_two(running_lst + [primes[i]]):
            prime_pair_sets(i + 1, running_lst + [primes[i]], primes)


def solve(limit):
    """Search primes below limit for the lowest-sum five-prime concatenation set."""
    primes = sieve_primes(limit)
    for i in range(len(primes)):
        prime_pair_sets(i + 1, [primes[i]], primes)


from mytimeit import *

with MyTimer() as t:
    import sys

    sys.setrecursionlimit(10**9)
    print(solve(10000))
