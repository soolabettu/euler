# Discovers numbered Python scripts, runs one by problem number, and normalizes its answer output.

from __future__ import annotations

import argparse
import subprocess
import sys
import time
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
        return _pick_answer_line(lines)


def _pick_answer_line(lines: list[str]) -> str:
    """Return the most likely answer line from script output.

    Many local scripts also print timing lines (e.g. "Elapsed time: ...").
    We skip those and return the last remaining line.
    """
    timing_prefixes = (
        "elapsed",
        "elapsed time",
        "program took",
        "time taken",
        "runtime",
        "duration",
    )
    for line in reversed(lines):
        lower = line.lower()
        if any(lower.startswith(prefix) for prefix in timing_prefixes):
            continue
        return line
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


def solve_problem_with_timing(problem_number: int) -> tuple[str, float]:
    start = time.perf_counter()
    result = solve_problem(problem_number)
    elapsed = time.perf_counter() - start
    return result, elapsed


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Run a Project Euler Python solution by problem number (excluding 650.py)."
        )
    )
    parser.add_argument(
        "problem",
        nargs="?",
        type=int,
        help="Project Euler problem number",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all discovered solved Python problem numbers.",
    )
    args = parser.parse_args()

    if args.list:
        print(" ".join(map(str, sorted(SOLUTION_CLASSES))))
        return

    if args.problem is None:
        parser.error("the following arguments are required: problem (or use --list)")

    try:
        result, elapsed = solve_problem_with_timing(args.problem)
        print(result)
        print(f"Elapsed: {elapsed:.6f}s")
    except ValueError as exc:
        parser.exit(status=2, message=f"{exc}\n")


if __name__ == "__main__":
    main()
