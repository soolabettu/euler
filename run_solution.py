from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from solution import Solution

ROOT = Path(__file__).resolve().parent


class ScriptSolution(Solution):
    script_path: Path

    def solve(self) -> str:
        completed = subprocess.run(
            [sys.executable, str(self.script_path)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            check=True,
        )
        output = completed.stdout.strip()
        if not output:
            return ""
        lines = [line.strip() for line in output.splitlines() if line.strip()]
        return lines[-1] if lines else ""


def _discover_solution_classes() -> dict[int, type[Solution]]:
    solution_classes: dict[int, type[Solution]] = {}
    for path in sorted(ROOT.glob("*.py")):
        if not path.stem.isdigit():
            continue
        if path.name == "650.py":
            continue
        problem_number = int(path.stem)
        class_name = f"Problem{problem_number}Solution"
        solution_class = type(
            class_name,
            (ScriptSolution,),
            {
                "problem_number": problem_number,
                "script_path": path,
                "__module__": __name__,
            },
        )
        solution_classes[problem_number] = solution_class
        globals()[class_name] = solution_class
    return solution_classes


SOLUTION_CLASSES = _discover_solution_classes()


def get_solution(problem_number: int) -> Solution:
    try:
        return SOLUTION_CLASSES[problem_number]()
    except KeyError as exc:
        available = ", ".join(str(p) for p in sorted(SOLUTION_CLASSES))
        raise ValueError(
            f"No Python solution found for problem {problem_number}. Available: {available}"
        ) from exc


def solve_problem(problem_number: int) -> str:
    return get_solution(problem_number).solve()


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Run a Project Euler Python solution by problem number (excluding 650.py)."
        )
    )
    parser.add_argument("problem", type=int, help="Project Euler problem number")
    args = parser.parse_args()

    try:
        print(solve_problem(args.problem))
    except ValueError as exc:
        parser.exit(status=2, message=f"{exc}\n")


if __name__ == "__main__":
    main()
