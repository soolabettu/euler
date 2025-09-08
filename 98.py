import sympy
from collections import defaultdict


def sort_by_length(words):
    return sorted(words, key=len, reverse=True)


def read_data():
    with open("98.txt") as f:
        data = f.read()
        words = [w.strip('"') for w in data.split(",")]

    words = sort_by_length(words)

    return words


from itertools import permutations


def go(words):
    for w in words:
        for p in permutations(w):
            # print(p)
            w1 = "".join(p)
            if w1 != w and w1 in words:
                # print(w, p)
                return

    return


def square_numbers():
    i = 1
    nums = []
    while True:
        i += 1
        if len(str(i * i)) > 9:
            break

        nums.append(i * i)

    return nums


def digits_unique(s: str) -> bool:
    # Keep only digits
    digits = [ch for ch in s if ch.isdigit()]
    return len(digits) == len(set(digits))


def reverse_map_word(mapping, digit_string):
    # Reverse the dictionary: numbers → letters
    reversed_map = {v: k for k, v in mapping.items()}

    # Build the word by replacing each digit with its mapped letter
    try:
        word = "".join(reversed_map[d] for d in digit_string)
    except KeyError:
        return None

    return word


def is_bijective_mapping(digits: str, letters: str) -> bool:
    if len(digits) != len(letters):
        return (
            False,
            {},
            {},
        )

    d2l = {}
    l2d = {}

    for d, l in zip(digits, letters):
        # if digit already mapped, must match same letter
        if d in d2l and d2l[d] != l:
            return (False, d2l, l2d)
        # if letter already mapped, must match same digit
        if l in l2d and l2d[l] != d:
            return (False, d2l, l2d)

        d2l[d] = l
        l2d[l] = d

    # Reconstruct digit string from letters and l2d mapping
    reconstructed = "".join(l2d[l] for l in letters)
    return (reconstructed == digits, d2l, l2d)


from collections import defaultdict


def check_anagrams(words):
    """
    For every word in the list, check if there exists
    another word in the list that is its anagram.
    Returns a dict: word -> True/False
    """
    # Group words by sorted letters (canonical form)
    groups = defaultdict(list)
    for w in words:
        key = "".join(sorted(w))
        groups[key].append(w)

    # A word has an anagram in the list if its group has >1 element
    result = {w: (groups["".join(sorted(w))]) for w in words}
    return result


# Example
words = ["listen", "silent", "enlist", "rat", "tar", "art", "hello"]


def solve():
    words = read_data()
    nums = square_numbers()
    nums = sorted(nums, reverse=True)
    ans = 0
    done = defaultdict(bool)

    anagrams = check_anagrams(words)
    for word in words:
        if len(anagrams[word]) == 1:
            continue

        if done[str(sorted(word))]:
            continue

        for word1 in anagrams[word]:

            if word1 == word:
                continue

            nums1 = [num for num in nums if len(str(num)) == len(word1)]
            for num in nums1:
                is_it, d2l, l2d = is_bijective_mapping(str(num), word1)
                if not is_it:
                    continue

                for x in nums1:
                    if x == num:
                        continue

                    if sorted(str(num)) == sorted(str(x)):

                        reconstructed = reverse_map_word(l2d, str(x))
                        if reconstructed in anagrams[word]:
                            print(
                                "Candidate solution {}, {}, {}, {}".format(
                                    word, reconstructed, num, x
                                )
                            )
                            ans = max(ans, max(num, x))
                            flag = False
                            break

        done[str(sorted(word))] = True

    return ans


from mytimeit import *

with MyTimer() as t:
    print(solve())
