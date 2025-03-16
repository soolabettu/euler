#!/usr/bin/env python3

from mytimeit import *
import time


def is_palindrome(n):
    return str(n) == str(n)[::-1]


def reverse_and_add(n):
    return n + int(str(n)[::-1])


def solve():
    def is_lychrel(n, max_iterations=50):
        """
        Checks if a number 'n' is a Lychrel candidate by performing
        reverse-and-add for up to max_iterations times. If a palindrome
        is found, return False (not Lychrel). Otherwise, return True.
        """
        temp = n
        for _ in range(max_iterations):
            temp = reverse_and_add(temp)
            if is_palindrome(temp):
                return False
        return True

    count_lychrels = 0
    lychrel_list = []
    for num in range(1, 10000):
        if is_lychrel(num):
            count_lychrels += 1
            lychrel_list.append(num)

    print("Count of Lychrel candidates under 10,000:", count_lychrels)
    # print("Lychrel candidates:", lychrel_list)


if __name__ == "__main__":
    with MyTimer(solve) as timer:
        solve()
