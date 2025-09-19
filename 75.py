from collections import defaultdict

from sympy import isprime

from math import gcd


def pythagorean_triplets_perimeter(limit, primitive_only=False):
    """
    Yield all Pythagorean triples (a, b, c) with a < b < c, a^2 + b^2 = c^2,
    and a + b + c <= limit.

    If primitive_only=True, only primitive triples are yielded.
    """
    if limit < 12:  # smallest perimeter is 3-4-5 -> 12
        return

    # Primitive triples: (a0,b0,c0) = (m^2-n^2, 2mn, m^2+n^2),
    # with m>n>=1, gcd(m,n)=1, and m-n odd. Scale by k>=1 while k*P0 <= limit.
    # Perimeter P0 = 2*m*(m+n).
    m_max = int((limit // 2) ** 0.5)  # since 2*m*(m+n) <= limit

    for m in range(2, m_max):
        for n in range(1, m):
            if (m - n) % 2 == 0 or gcd(m, n) != 1:
                continue  # ensure primitive
            a0 = m * m - n * n
            b0 = 2 * m * n
            c0 = m * m + n * n
            if a0 > b0:
                a0, b0 = b0, a0  # enforce a<b
            P0 = a0 + b0 + c0  # equals 2*m*(m+n)

            if P0 > limit:
                continue

            k = 1
            while k * P0 <= limit:
                a, b, c = k * a0, k * b0, k * c0
                if not primitive_only or k == 1:
                    yield (a, b, c)
                k += 1


# --- demo ---
def solve(limit):
    triples = sorted(pythagorean_triplets_perimeter(limit), key=lambda t: (sum(t), t))
    print(f"{len(triples)} triples with a+b+c <= {limit}:")
    my_dict = defaultdict(int)
    for t in triples:
        # print(f"{t}  (perimeter={sum(t)})")
        my_dict[t[0] + t[1] + t[2]] += 1

    cnt = 0
    for k, v in my_dict.items():
        if v == 1:
            print(k, v)
            cnt += 1

    print(cnt)
    # --- solution ---
    # my_dict = defaultdict(list)
    # for i in range(1, limit):
    #    my_dict[i] = pythagorean_triples_with_sum(i)

    # sorted_dict = {k: v for k, v in sorted(my_dict.items(), key=lambda item: len(item[1]), reverse=True)}

    # for k, v in my_dict.items():
    #    if len(v) == 2:
    #        print(k, v)


from mytimeit import MyTimer

with MyTimer() as t:
    solve(1500000)
