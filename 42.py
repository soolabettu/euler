#!/usr/bin/env python3
# Scores words from input and counts those whose values are triangular numbers.

"""Project Euler Problem 42: https://projecteuler.net/problem=42"""


def solve():
    """Count triangle words in the provided list."""

    def is_triangle_number(y, x=1, i=1):
        """Return True if y is a triangular number."""
        while x < y:
            x = (i * (i + 1)) // 2
            i += 1

        return x == y

    f = open("./0042_words.txt", "r")
    print(
        len(
            list(
                filter(
                    is_triangle_number,
                    [
                        sum(ord(c) - 64 for c in w)
                        for w in [
                            w
                            for w in [
                                word.replace('"', "")
                                for word in [
                                    word.replace('"', "")
                                    for word in f.read().strip().split(",")
                                ]
                            ]
                        ]
                    ],
                )
            )
        )
    )


if __name__ == "__main__":
    solve()
