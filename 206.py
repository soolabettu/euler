from math import isqrt
from typing import List, Tuple, Optional

import math


def check_concatenation_forms_target(s, target="123456789"):
    """
    Check if every other character from position 0, when concatenated,
    forms the target string.

    Args:
        s (str): Input string to check
        target (str): Target string to match (default: "123456789")

    Returns:
        bool: True if concatenated characters match the target
    """
    # Extract every other character starting from position 0
    extracted_chars = s[::2]  # This is equivalent to s[0::2]

    # Check if it matches the target
    return extracted_chars == target


def solve(limit):
    """Search for the unique square below limit whose pattern matches 1_2_3_4_5_6_7_8_9."""
    x = 10**8 + 3
    product = 1
    while True:
        product = x * x
        if x % 10 == 7:
            x += 6
        elif x % 10 == 3:
            x += 4

        if product > limit:
            break
        elif len(str(product)) == 17 and check_concatenation_forms_target(str(product)):
            print(product)
            break


from mytimeit import MyTimer

with MyTimer() as t:
    solve(10**19)
