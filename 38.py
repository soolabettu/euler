import mytimeit


def solve() -> int:
    """Return the largest pandigital concatenated product."""
    max_prod = 0
    for i in range(99999, 1, -1):
        prod = ""
        for j in range(1, 10):
            prod += str(i * j)
            if len(prod) > 9:
                break

            if len(prod) == 9:
                sorted_prod = sorted(prod, key=int)
                if "".join(sorted_prod) == "123456789":
                    max_prod = max(int(prod), max_prod)

    return max_prod


with mytimeit.MyTimer() as t:
    print(solve())
