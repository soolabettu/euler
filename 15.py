#!/usr/bin/env python3
# Fills a lattice-path dynamic-programming table for a 20x20 grid.

"""Project Euler Problem 15: https://projecteuler.net/problem=15"""


import math

ans = 0
num = 0
sz = 21
matrix = [[0 for _ in range(sz)] for _ in range(sz)]
for i in range(sz):
    matrix[i][0] = 1
    matrix[0][i] = 1
    matrix[sz - 1][i] = 1
    matrix[i][sz - 1] = 1

for i in range(1, sz):
    for j in range(1, sz):
        matrix[i][j] = matrix[i - 1][j] + matrix[i][j - 1]

print(matrix[sz - 1][sz - 1])
