import math


def roman_to_int(roman: str) -> int:
    """Convert a Roman numeral (even additive forms) to integer."""
    values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}

    total = 0
    i = 0
    while i < len(roman):
        # If this character is smaller than the next, it's subtractive
        if i + 1 < len(roman) and values[roman[i]] < values[roman[i + 1]]:
            total += values[roman[i + 1]] - values[roman[i]]
            i += 2
        else:
            total += values[roman[i]]
            i += 1
    return total


def int_to_minimal_roman(num: int) -> str:
    """Convert integer to minimal (canonical) Roman numeral."""
    val_map = [
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    ]

    result = []
    for value, symbol in val_map:
        while num >= value:
            result.append(symbol)
            num -= value
    return "".join(result)


def simplify_roman(roman: str) -> str:
    """Return the number of characters saved by writing the numeral in minimal form."""
    return len(roman) - len(int_to_minimal_roman(roman_to_int(roman)))


def solve(limit):
    """Compute the total characters saved by minimizing the provided Roman numerals."""
    ans = 0
    with open("89.txt") as f:
        data = f.read()
        ans = sum([simplify_roman(n) for n in data.split("\n")])

    return ans


import mytimeit

with mytimeit.MyTimer() as t:
    print(solve(100))
