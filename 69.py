import mytimeit


def totients_up_to(n: int):
    """
    Returns a list phi where phi[x] = φ(x) for x=0..n (phi[0] is 0 by convention).
    Complexity: ~ O(n log log n)
    """
    if n < 1:
        return [0] * (n + 1)
    phi = list(range(n + 1))  # initialize φ(i) = i
    for p in range(2, n + 1):
        if phi[p] == p:  # p is prime
            step = p
            for k in range(p, n + 1, step):
                phi[k] -= phi[k] // p
    phi[0] = 0
    phi[1] = 1
    return phi


# Example
def solve(N):
    x = totients_up_to(N)
    result = 0
    max_n = 0
    for i in range(2, N):
        if result < i / x[i]:
            result = i / x[i]
            max_n = i
        result = max(result, i / x[i])

    return max_n


with mytimeit.MyTimer() as t:
    print(solve(1000000))
