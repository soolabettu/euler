from mytimeit import MyTimer

from math import comb

mod = 10**16


def partitions(n, max_val=None):
    """Yield every integer partition of ``n`` in non-increasing order.

    Parameters
    ----------
    n : int
        Target integer to be partitioned.
    max_val : int | None, optional
        Maximum part size allowed for the current recursion branch. When
        ``None`` the value defaults to ``n``, ensuring that partitions are
        emitted in non-increasing order.

    Yields
    ------
    list[int]
        A list of positive integers whose sum is ``n`` and whose elements are
        sorted in non-increasing order.
    """
    if max_val is None:
        max_val = n
    if n == 0:
        yield []
    else:
        for i in range(min(max_val, n), 0, -1):
            for tail in partitions(n - i, i):
                yield [i] + tail


from collections import Counter


def unique_perm_count(lst):
    """Return the weighted multiplicity of permutations of ``lst``.

    For a multiset of digits ``lst`` this function computes the quantity
    ``sum(lst) * (len(lst) - 1)!`` adjusted for repeated elements. The result
    represents the total contribution of the digits to a fixed position across
    all unique permutations (e.g. the sum of digits that appear in the units
    position over every distinct ordering).

    Parameters
    ----------
    lst : list[int]
        Multiset of digits whose permutations are considered.

    Returns
    -------
    int
        Total weighted count described by
        ``factorial(len(lst) - 1) * sum(lst) / prod(factorial(counts))``.
    """
    n = len(lst)
    counts = Counter(lst).values()
    denom = 1
    for c in counts:
        denom *= factorial(c)
    num = factorial(n - 1) * sum(lst)
    return num // denom


from math import factorial


def solve(perm, limit):
    """Sum the contributions of ``perm`` permutations padded with zeros.

    The function evaluates, modulo ``10**16``, the cumulative value of all
    distinct numbers that can be formed by permuting the digits in ``perm`` and
    inserting between ``0`` and ``limit - len(perm)`` trailing zeros. The
    calculation leverages combinatorial identities to aggregate contributions
    per digit position instead of enumerating every permutation.

    Parameters
    ----------
    perm : list[int]
        Base multiset of non-zero digits to permute.
    limit : int
        Maximum total length allowed for the numbers, including appended zeros.

    Returns
    -------
    int
        Sum of the generated numbers modulo ``10**16``.
    """
    n = len(perm)
    sum_over_all_zeros = 0
    k_limit = limit - n
    for k in range(0, k_limit + 1):
        grand_total = 0

        def for_all_digit_positions(n, k):
            """Aggregate digit contributions for every position with k zeros.

            Parameters
            ----------
            n : int
                Number of non-zero digits drawn from ``perm``.
            k : int
                Count of appended zeros under consideration.

            Returns
            -------
            int
                Positional contribution of all digit permutations modulo ``mod``.
            """
            ans = 0
            for i in range(1, n + 1):

                def C_ni_k(n, i, k):
                    """Helper to count digit shifts when appending zeros.

                    Parameters
                    ----------
                    n : int
                        Number of non-zero digits.
                    i : int
                        Current digit position (1-indexed).
                    k : int
                        Number of zeros added to the permutation.

                    Returns
                    -------
                    int
                        Weighted sum of shifted combinations for the position.
                    """
                    ans = 0
                    for b in range(0, min(17, k + 1)):
                        ans = (
                            ans
                            + (
                                comb(max(i + k - b - 2, 0), k - b)
                                * comb(n - i + b, b)
                                % mod
                            )
                            * pow(10, b, mod)
                        ) % mod

                    return ans

                ans = ans + pow(10, n - i, mod) * C_ni_k(n, i, k) % mod
            return ans

        ans = for_all_digit_positions(n, k)
        sum_over_all_zeros = (sum_over_all_zeros + ans * unique_perm_count(perm)) % mod

    return int(sum_over_all_zeros)


with MyTimer() as t:
    for limit in range(2020, 2021):
        ans = 0
        for i in range(1, 10):
            parts = partitions(i)
            for p in parts:
                x = p + [i]
                if len(x) <= limit:
                    ans = (ans + solve(x, limit)) % mod

        print(ans)
