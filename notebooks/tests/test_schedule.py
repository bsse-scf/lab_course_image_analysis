"""detailed_schedule.md must agree with the course material.

The schedule is the single source of truth for what is taught where. If a
notebook heading changes without the schedule changing (or vice versa), this
fails, which is the whole point of having a source of truth.
"""

import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
SCHEDULE = REPO / ".course" / "solutions" / "detailed_schedule.md"


def test_schedule_matches_material():
    if not SCHEDULE.exists():
        pytest.skip("detailed_schedule.md lives in the solutions submodule, which is not checked out")
    result = subprocess.run(
        [sys.executable, str(REPO / ".course" / "scripts" / "check_schedule.py")],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
