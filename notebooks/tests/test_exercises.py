"""Guards on the generated exercise notebooks.

These catch the two ways the blanks convention can fail silently: a solution
leaking into a notebook students open, and a generated file drifting from the
solution it came from because someone hand-edited it.
"""

import subprocess
import sys
import warnings
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


@pytest.mark.parametrize("path", EXERCISES, ids=_ids(EXERCISES))
def test_has_a_solution_source(path):
    """Every exercise must be generated, not hand-written."""
    source = (REPO / "solutions" / "python" /
              path.name.replace("_ex.ipynb", "_ex_solution.ipynb"))
    if not source.exists():
        pytest.skip(f"{source.name} not present (solutions are gitignored)")
    assert source.exists()


SOLUTIONS = REPO / "solutions" / "python"
HAVE_SOLUTIONS = SOLUTIONS.is_dir() and any(SOLUTIONS.glob("*_ex_solution.ipynb"))


def test_generated_exercises_are_current(recwarn):
    """Regenerating must be a no-op - otherwise someone edited a generated file.

    `solutions/` is a submodule that most checkouts cannot read, so this check
    can only run for instructors. It warns rather than fails when the submodule
    is absent, because a silent skip would let the exercises drift out of sync
    with the solutions and nobody would notice.
    """
    if not HAVE_SOLUTIONS:
        warnings.warn(
            "solutions/ submodule is not checked out, so the generated exercises "
            "CANNOT be verified against their solutions. Run "
            "`git submodule update --init` and `pixi run sync-solutions` before "
            "trusting notebooks/*_ex.ipynb.",
            UserWarning,
            stacklevel=2,
        )
        pytest.skip("solutions submodule not available - see the warning above")

    result = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "make_exercises.py"), "--check"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
