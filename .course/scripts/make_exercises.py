"""Generate student exercise notebooks from the instructor solutions.

Solutions live in `.course/solutions/python/<name>_ex_solution.ipynb` and are the single
source of truth. `course.py` is importable from there because pixi puts
`notebooks/` on PYTHONPATH. This script strips the solution blocks and emits the blank notebooks
that students actually open.

    pixi run make-exercises            # regenerate all
    pixi run make-exercises --check    # fail if anything is out of date (CI)

Markers, inside a code cell:

    # --- your turn ---
    ### BEGIN SOLUTION
    thresh = threshold_otsu(nuclei)
    ### END SOLUTION
    ### BEGIN PROMPT
    # thresh = ...   # TODO: compute an Otsu threshold for `nuclei`
    ### END PROMPT

The SOLUTION block is dropped and the PROMPT block is uncommented in its place.
A cell tagged `solution-only` is removed from the exercise entirely.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import nbformat

REPO = Path(__file__).resolve().parents[2]
NOTEBOOKS = REPO / "notebooks"
SOLUTIONS = REPO / ".course" / "solutions" / "python"
SOLUTION_GLOB = "*_ex_solution.ipynb"

BEGIN_SOLUTION = "### BEGIN SOLUTION"
END_SOLUTION = "### END SOLUTION"
BEGIN_PROMPT = "### BEGIN PROMPT"
END_PROMPT = "### END PROMPT"


def _uncomment(line: str) -> str:
    """Strip one leading comment marker from a PROMPT line."""
    stripped = line.lstrip()
    if not stripped.startswith("#"):
        return line
    indent = line[: len(line) - len(stripped)]
    body = stripped[1:]
    if body.startswith(" "):
        body = body[1:]
    return indent + body


def strip_source(source: str) -> str:
    """Drop SOLUTION blocks and uncomment PROMPT blocks."""
    out: list[str] = []
    mode = "copy"

    for line in source.splitlines():
        marker = line.strip()

        if marker == BEGIN_SOLUTION:
            mode = "solution"
            continue
        if marker == END_SOLUTION:
            mode = "copy"
            continue
        if marker == BEGIN_PROMPT:
            mode = "prompt"
            continue
        if marker == END_PROMPT:
            mode = "copy"
            continue

        if mode == "solution":
            continue
        if mode == "prompt":
            out.append(_uncomment(line))
        else:
            out.append(line)

    if mode != "copy":
        raise ValueError(f"unterminated {mode.upper()} block")

    return "\n".join(out)


def build_exercise(nb):
    """Return a copy of ``nb`` with solutions stripped and outputs cleared."""
    cells = []
    for index, cell in enumerate(nb.cells):
        tags = cell.get("metadata", {}).get("tags", [])
        if "solution-only" in tags:
            continue

        cell = nbformat.from_dict(cell)
        if cell.cell_type == "code":
            try:
                cell.source = strip_source(cell.source)
            except ValueError as exc:
                raise ValueError(f"cell {index}: {exc}") from exc
            cell.outputs = []
            cell.execution_count = None

        cells.append(cell)

    nb = nbformat.from_dict(nb)
    nb.cells = cells
    nb.metadata.pop("widgets", None)
    return nb


def leaked_markers(nb) -> bool:
    """True if any solution marker survived into the generated notebook."""
    return any(
        marker in cell.source
        for cell in nb.cells
        for marker in (BEGIN_SOLUTION, END_SOLUTION, BEGIN_PROMPT, END_PROMPT)
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify generated notebooks are up to date instead of writing them",
    )
    args = parser.parse_args()

    if not SOLUTIONS.is_dir():
        print(f"No solutions directory at {SOLUTIONS} - nothing to do.")
        return 0

    sources = sorted(SOLUTIONS.glob(SOLUTION_GLOB))
    if not sources:
        print(f"No {SOLUTION_GLOB} files in {SOLUTIONS} - nothing to do.")
        return 0

    stale = []
    for source in sources:
        nb = nbformat.read(source, as_version=4)
        try:
            exercise = build_exercise(nb)
        except ValueError as exc:
            print(f"error: {source.name}: {exc}", file=sys.stderr)
            return 2

        if leaked_markers(exercise):
            print(f"error: {source.name}: solution marker leaked into output", file=sys.stderr)
            return 2

        target = NOTEBOOKS / source.name.replace("_solution.ipynb", ".ipynb")
        rendered = nbformat.writes(exercise, version=4).rstrip() + "\n"

        if args.check:
            current = target.read_text(encoding="utf-8") if target.exists() else ""
            if current.rstrip() + "\n" != rendered:
                stale.append(target.name)
            continue

        target.write_text(rendered, encoding="utf-8", newline="\n")
        print(f"wrote {target.relative_to(REPO)}")

    if args.check:
        if stale:
            print(
                "error: these exercise notebooks are out of date - "
                f"run `pixi run make-exercises`: {', '.join(stale)}",
                file=sys.stderr,
            )
            return 1
        print(f"{len(sources)} exercise notebook(s) up to date.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
