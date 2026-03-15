# Defines the abstract base interface implemented by callable Euler solutions.

from __future__ import annotations

from abc import ABC, abstractmethod


class Solution(ABC):
    problem_number: int

    @abstractmethod
    def solve(self) -> str:
        raise NotImplementedError
