"""Find palindromic sums of selected squares and cubes."""

from collections import Counter
from time import perf_counter


start_time = perf_counter()

# All two-, three-, four-, and five-digit numbers (10 through 99,999).
squares = {number**2 for number in range(10, 100_000)}

# All two- and three-digit numbers (10 through 999).
cubes = {number**3 for number in range(10, 1_000)}


def build_palindromes(minimum: int, maximum: int) -> set[int]:
    """Return every palindrome in the inclusive interval."""
    palindromes = set()
    prefix = 1

    while True:
        digits = str(prefix)
        odd_length = int(digits + digits[-2::-1])
        even_length = int(digits + digits[::-1])

        if odd_length > maximum and even_length > maximum:
            break

        if minimum <= odd_length <= maximum:
            palindromes.add(odd_length)
        if minimum <= even_length <= maximum:
            palindromes.add(even_length)

        prefix += 1

    return palindromes


def build_palindromic_sum_counts(
    square_values: set[int], cube_values: set[int]
) -> tuple[tuple[int, int], ...]:
    """Return (palindromic sum, count) tuples for square-cube pairs."""
    palindrome_candidates = build_palindromes(
        min(square_values) + min(cube_values),
        max(square_values) + max(cube_values),
    )
    frequencies: Counter[int] = Counter()

    for square in square_values:
        for cube in cube_values:
            total = square + cube
            if total in palindrome_candidates:
                frequencies[total] += 1

    return tuple(frequencies.items())


# Only palindromic totals are retained, keeping memory bounded for 99 million pairs.
palindromic_sum_counts = build_palindromic_sum_counts(squares, cubes)
palindromic_sums_with_count_4 = tuple(
    entry for entry in palindromic_sum_counts if entry[1] == 4
)
sum_of_palindromic_sums = sum(
    total for total, _ in palindromic_sums_with_count_4
)
elapsed_seconds = perf_counter() - start_time


if __name__ == "__main__":
    print(f"Stored {len(squares):,} squares in the squares set.")
    print(f"Smallest square: {min(squares):,}")
    print(f"Largest square:  {max(squares):,}")

    print(f"\nStored {len(cubes):,} cubes in the cubes set.")
    print(f"Smallest cube: {min(cubes):,}")
    print(f"Largest cube:  {max(cubes):,}")

    print(f"\nChecked {len(squares) * len(cubes):,} square-cube pairings.")
    print(f"Found {len(palindromic_sum_counts):,} distinct palindromic sums.")
    print("Each entry has the form (palindromic_sum, occurrence_count).")

    print(
        "\nPalindromic sums formed exactly four times: "
        f"{len(palindromic_sums_with_count_4):,}"
    )
    matching_sums = sorted(total for total, _ in palindromic_sums_with_count_4)
    print(f"Matching sums: {matching_sums}")
    print(f"Sum of matching palindromes: {sum_of_palindromic_sums:,}")
    print(f"Elapsed time: {elapsed_seconds:.3f} seconds")
