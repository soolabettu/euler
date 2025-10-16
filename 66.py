import math

from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Step:
    """Single iteration values from the continued fraction expansion of √N."""
    k: int
    m: int
    d: int
    a: int


def cf_sqrt(N: int) -> Tuple[int, List[int], List[Step]]:
    """Return the continued fraction expansion components for √N."""
    a0 = int(N**0.5)
    m = 0
    d = 1
    a = a0
    steps = [Step(k=0, m=m, d=d, a=a)]
    period = []
    m_k, d_k, a_k = m, d, a
    while True:
        m_next = d_k * a_k - m_k
        d_next = (N - m_next * m_next) // d_k
        a_next = (a0 + m_next) // d_next
        period.append(a_next)
        steps.append(Step(k=len(steps), m=m_next, d=d_next, a=a_next))
        if a_next == 2 * a0 and d_next == 1:
            break
        m_k, d_k, a_k = m_next, d_next, a_next
    return a0, period, steps


def convergents_from_cf(
    a0: int, a_list: List[int], upto_k: int
) -> List[Tuple[int, int]]:
    """Build convergents from the continued-fraction digits up to index upto_k."""
    p_minus2, p_minus1 = 0, 1
    q_minus2, q_minus1 = 1, 0
    convergents = []
    digits = [a0] + a_list
    for k in range(upto_k + 1):
        ak = digits[k]
        pk = ak * p_minus1 + p_minus2
        qk = ak * q_minus1 + q_minus2
        convergents.append((pk, qk))
        p_minus2, p_minus1 = p_minus1, pk
        q_minus2, q_minus1 = q_minus1, qk
    return convergents


def pell_fundamental_solution(N: int):
    """Compute the minimal solution to x^2 - N*y^2 = 1."""
    a0, period, steps = cf_sqrt(N)
    L = len(period)
    if L % 2 == 0:
        k = L - 1
        repeat_digits = period
    else:
        k = 2 * L - 1
        repeat_digits = period + period
    convs = convergents_from_cf(a0, repeat_digits, k)
    x, y = convs[k]
    return (x, y), k, L, steps


def solve(n):
    """Find the D ≤ n that generates the largest minimal x in Pell's equation."""
    ans = 0
    result = 0
    for i in range(n + 1):
        if is_perfect_square(i):
            continue
        (x, y), k_idx, L, steps = pell_fundamental_solution(i)
        if ans < x:
            ans = x
            result = i

    return result


def is_perfect_square(n: int) -> bool:
    """Return True if n is a perfect square."""
    if n < 0:
        return False  # negative numbers can't be perfect squares
    root = math.isqrt(n)  # integer square root (floor of sqrt(n))
    return root * root == n


from mytimeit import *

with MyTimer() as t:
    print(solve(1000))
