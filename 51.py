def sieve_of_eratosthenes(limit):
    """Generate all prime numbers up to 'limit' using the Sieve of Eratosthenes."""
    sieve = [True] * (limit + 1)  # Assume all numbers are prime initially
    sieve[0] = sieve[1] = False  # 0 and 1 are not prime

    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            # Mark multiples of i as not prime
            for j in range(i * i, limit + 1, i):
                sieve[j] = False

    # Collect all primes
    return [i for i, is_prime in enumerate(sieve) if is_prime]


def replace_occurrences(s, target, replacement):
    """Return a new string replacing every target character with replacement."""
    count = 0
    s_list = list(s)  # make string mutable
    for i, ch in enumerate(s_list):
        if ch == target:
            s_list[i] = replacement
            count += 1
    new_s = "".join(s_list)
    return new_s


import mytimeit
from collections import defaultdict

with mytimeit.MyTimer() as t:
    primes = sieve_of_eratosthenes(1000000)
    print(f"Number of primes found: {len(primes)}")
    for p in primes:
        max_cnt = 0
        for i in range(10):
            cnt = 1
            if str(p).count(str(i)) > 1:
                for j in range(10):
                    if i == j:
                        continue
                    next_prime = replace_occurrences(str(p), str(i), str(j))
                    if next_prime[0] == "0":
                        continue
                    if int(next_prime) in primes:
                        cnt += 1
            max_cnt = max(max_cnt, cnt)

        if max_cnt == 8:
            print(p)
            break
