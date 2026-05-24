MOD = 1234567890


def grundy_bucket_sizes(limit: int) -> list[int]:
    """Count how many values 1..limit have each Grundy number.

    For this game the Grundy number of x is v2(x), the exponent of 2 in x.
    That partitions 1..limit into buckets:

    - bucket 0: odd numbers
    - bucket 1: divisible by 2 but not by 4
    - bucket 2: divisible by 4 but not by 8
    - ...

    The count in bucket k is:

        floor(limit / 2^k) - floor(limit / 2^(k + 1))

    until the final bucket, which contains the powers-of-two tail where
    2^k <= limit < 2^(k + 1).
    """
    powers_of_two: list[int] = []
    power = 2

    # Collect the powers of two strictly below the limit so we can compute
    # successive "divisible by 2^k but not by 2^(k+1)" bucket sizes.
    while power < limit:
        powers_of_two.append(power)
        power *= 2

    # Handle the smallest bucket separately: numbers not divisible by 2.
    buckets = [limit - limit // 2]

    # Middle buckets: divisible by the current power of two, but not the next.
    for current, nxt in zip(powers_of_two, powers_of_two[1:]):
        buckets.append(limit // current - limit // nxt)

    # Final bucket: numbers divisible by the largest power of two below limit.
    # This is the highest possible Grundy value for the given bound.
    buckets.append(limit // powers_of_two[-1])

    return buckets


def count_winning_positions(bucket_sizes: list[int]) -> int:
    """Count ordered triples whose xor is non-zero.

    If bucket_sizes[g] tells us how many pile sizes have Grundy number g, then
    every ordered pile triple contributes according to the product of the three
    selected bucket sizes. A position is winning iff the xor of the three
    Grundy values is non-zero.
    """
    total = 0

    for left_grundy, left_count in enumerate(bucket_sizes):
        for middle_grundy, middle_count in enumerate(bucket_sizes):
            for right_grundy, right_count in enumerate(bucket_sizes):
                if left_grundy ^ middle_grundy ^ right_grundy:
                    total += left_count * middle_count * right_count
                    total %= MOD

    return total


def solve(limit: int) -> int:
    """Return S(limit) modulo MOD for the current counting strategy."""
    bucket_sizes = grundy_bucket_sizes(limit)
    return count_winning_positions(bucket_sizes)


if __name__ == "__main__":
    N = 123456787654321
    print(solve(N))
