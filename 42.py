#!/usr/bin/env python3


from mytimeit import *
import time


def solve():

    def is_triangle_number(y, x=1, i=1):
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
    with MyTimer(solve) as timer:
        solve()
