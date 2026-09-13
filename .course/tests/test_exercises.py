"""Guards on the generated exercise notebooks.

These catch the two ways the blanks convention can fail silently: a solution
leaking into a notebook students open, and a generated file drifting from the
solution it came from because someone hand-edited it.
"""

import subprocess
import sys
from pathlib import Path

import nbformat
import pytest

REPO = Path(__file__).resolve().parents[2]
NOTEBOOKS = REPO / "notebooks"

MARKERS = ("### BEGIN SOLUTION", "### END SOLUTION", "### BEGIN PROMPT", "### END PROMPT")

EXERCISES = sorted(p for p in NOTEBOOKS.glob("*_ex.ipynb"))


def _ids(paths):
    return [p.name for p in paths]


@pytest.mark.parametrize("path", EXERCISES, ids=_ids(EXERCISES))
def test_no_solution_markers(path):
    nb = nbformat.read(path, as_version=4)
    for index, cell in enumerate(nb.cells):
        for marker in MARKERS:
            assert marker not in cell.source, f"{path.name} cell {index} still contains {marker}"


@pytest.mark.parametrize("path", EXERCISES, ids=_ids(EXERCISES))
def test_no_stored_outputs(path):
    """Exercises ship blank - a stored output means an answer is visible."""
    nb = nbformat.read(path, as_version=4)
    for index, cell in enumerate(nb.cells):
        if cell.cell_type == "code":
            assert not cell.outputs, f"{path.name} cell {index} has stored output"
            assert cell.execution_count is None, f"{path.name} cell {index} has an execution count"


SOLUTIONS = REPO / ".course" / "solutions" / "python"

#: The solutions live in a private submodule. These tests are instructor
#: tooling and CI has access, so a missing checkout is an error, not a skip: a
#: skipped check would let the exercises drift from the solutions unnoticed.
NO_SOLUTIONS = (
    f"{SOLUTIONS.relative_to(REPO).as_posix()} is not checked out; run "
    "`git submodule update --init` (needs access to the solutions repository)"
)


def test_solutions_submodule_is_checked_out():
    assert SOLUTIONS.is_dir() and any(SOLUTIONS.glob("*_ex_solution.ipynb")), NO_SOLUTIONS


@pytest.mark.parametrize("path", EXERCISES, ids=_ids(EXERCISES))
def test_has_a_solution_source(path):
    """Every exercise must be generated, not hand-written."""
    source = SOLUTIONS / path.name.replace("_ex.ipynb", "_ex_solution.ipynb")
    assert source.exists(), f"{path.name} has no solution at {source.relative_to(REPO)}"


def test_generated_exercises_are_current():
    """Regenerating must be a no-op - otherwise someone edited a generated file."""
    result = subprocess.run(
        [sys.executable, str(REPO / ".course" / "scripts" / "make_exercises.py"), "--check"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
