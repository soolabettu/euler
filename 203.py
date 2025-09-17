import mytimeit


def generate_pascals_triangle(n_rows):
    triangle = [[1]]  # Start with the first row
    unique_elements = set([1])  # Set of unique elements in the first row
    for _ in range(1, n_rows):
        prev_row = triangle[-1]
        next_row = [1]  # First element is always 1
        for i in range(1, len(prev_row)):
            next_row.append(prev_row[i - 1] + prev_row[i])
            unique_elements.add(prev_row[i - 1] + prev_row[i])
        next_row.append(1)  # Last element is always 1
        triangle.append(next_row)

    return unique_elements


# Example usage


def sieve_of_eratosthenes(limit):
    # Create a boolean array "prime[0..limit]" and initialize all entries as true.
    prime = [True] * (limit + 1)
    prime[0] = prime[1] = False  # 0 and 1 are not prime

    p = 2
    while p * p <= limit:
        if prime[p]:
            for i in range(p * p, limit + 1, p):
                prime[i] = False
        p += 1

    # Collect all prime numbers
    primes = [i for i, is_prime in enumerate(prime) if is_prime]
    return primes


from math import isqrt


def mobius(n):
    if n == 1:
        return 1

    prime_factors = 0
    i = 2
    while i <= isqrt(n):
        if n % i == 0:
            if (n // i) % i == 0:
                return 0  # Square factor found
            prime_factors += 1
            n //= i
        else:
            i += 1

    if n > 1:
        prime_factors += 1

    return -1 if prime_factors % 2 else 1


def solve():
    ans = 0
    rows = 51
    triangle = generate_pascals_triangle(rows)
    for r in triangle:
        if mobius(r) != 0:
            ans += r

    print(ans)


with mytimeit.MyTimer() as t:
    solve()
