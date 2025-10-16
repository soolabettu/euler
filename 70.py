from array import array
import mytimeit


def solve():
    """Find the number below ten million with minimal n/φ(n) among permutation totients."""

    def totients_upto(n: int):
        """
        Compute phi[0..n] where phi[k] = Euler's totient of k.
        Uses a multiplicative sieve in O(n log log n).
        Memory ~ 4*(n+1) bytes for the array (≈ 40 MB for n=10_000_000).
        """
        phi = array("I", [0]) * (n + 1)
        for i in range(n + 1):
            phi[i] = i

        for i in range(2, n + 1):
            if phi[i] == i:  # i is prime
                step = i
                for j in range(i, n + 1, step):
                    phi[j] -= phi[j] // i
        return phi

    from collections import Counter

    def is_permutation(s1: str, s2: str) -> bool:
        """Return True when the two strings are permutations of each other."""
        return Counter(s1) == Counter(s2)

    if __name__ == "__main__":
        N = 10_000_000
        phi = totients_upto(N)
        ans = 10**7

    import fractions

    result = 0
    for k in range(2, N + 1):
        if is_permutation(str(k), str(phi[k])):
            if fractions.Fraction(k, phi[k]) < ans:
                ans = fractions.Fraction(k, phi[k])
                result = k

    return result


with mytimeit.MyTimer() as t:
    print(solve())
