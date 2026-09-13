"""Keep detailed_schedule.md and the course materials in sync.

`detailed_schedule.md` is the single source of truth for what is taught where.
This script checks that every section it lists actually exists in the material,
and that no section of the material is missing from it.

    pixi run check-schedule          # report drift
    pixi run check-schedule --list   # print the headings as they are now

The check runs as part of `pixi run test`, so editing a notebook heading without
updating the schedule (or the reverse) fails loudly instead of quietly rotting.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import nbformat

REPO = Path(__file__).resolve().parents[2]
# The schedule lives in the private solutions submodule.
SCHEDULE = REPO / ".course" / "solutions" / "detailed_schedule.md"

HEADING = re.compile(r"^(#{1,3})\s+(.*?)\s*$")

#: Headings that are structural rather than content, and so are not listed
#: section-by-section in the schedule.
IGNORED = {"Recap", "If you finish early", "Preparation"}


def notebook_sections(path: Path) -> list[str]:
    """Level-2 headings of a notebook, in order."""
    nb = nbformat.read(path, as_version=4)
    out = []
    for cell in nb.cells:
        if cell.cell_type != "markdown":
            continue
        for line in cell.source.split("\n"):
            match = HEADING.match(line.strip())
            if match and len(match.group(1)) == 2:
                title = match.group(2)
                if title not in IGNORED:
                    out.append(title)
    return out


def markdown_sections(path: Path) -> list[str]:
    """Level-2 headings of a markdown page, in order."""
    out = []
    for line in path.read_text().split("\n"):
        match = HEADING.match(line.strip())
        if match and len(match.group(1)) == 2:
            title = match.group(2)
            if title not in IGNORED:
                out.append(title)
    return out


def material() -> dict[str, list[str]]:
    """Every teaching file, mapped to its section headings."""
    found: dict[str, list[str]] = {}
    for path in sorted((REPO / "notebooks").glob("*.ipynb")):
        # Solutions are instructor material; " copy" files are scratch working
        # copies that editors create and are not part of the course.
        if "_solution" in path.name or " copy" in path.name:
            continue
        found[f"notebooks/{path.name}"] = notebook_sections(path)
    for path in sorted((REPO / "book" / "fiji").rglob("*.md")):
        if path.name in {"index.md"} or path.name.startswith("cheat_sheet"):
            continue
        # as_posix(): on Windows str(Path) gives backslashes, which never
        # match the forward slashes used in detailed_schedule.md.
        found[path.relative_to(REPO).as_posix()] = markdown_sections(path)

    # Top-level book pages that carry teaching content. Navigation and
    # reference pages - landing, schedule, setup, further reading,
    # acknowledgements - are not scheduled section by section.
    for name in ("challenge.md", "homework.md"):
        path = REPO / "book" / name
        if path.exists():
            found[f"book/{name}"] = markdown_sections(path)
    return found


def scheduled() -> dict[str, list[str]]:
    """What detailed_schedule.md claims, parsed from its section tables.

    Each block starts with a line naming the file in backticks, and the sections
    are the first column of the table that follows.
    """
    if not SCHEDULE.exists():
        return {}

    claimed: dict[str, list[str]] = {}
    current: str | None = None
    for line in SCHEDULE.read_text().split("\n"):
        if line.startswith("#"):
            # A heading that names a file opens a block; any other heading
            # closes the previous one, so later tables are not misattributed.
            header = re.match(r"^#{2,4}\s+.*`((?:notebooks|book)/[^`]+)`", line)
            current = header.group(1) if header else None
            if current:
                claimed.setdefault(current, [])
            continue
        if current and line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if not cells or not cells[0]:
                continue
            first = cells[0]
            if first.startswith("---") or first.lower() in {"section", "task"}:
                continue
            claimed[current].append(first.strip("*` "))
    return claimed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="print current headings and exit")
    args = parser.parse_args()

    found = material()

    if args.list:
        for name, sections in found.items():
            print(f"\n{name}")
            for s in sections:
                print(f"  - {s}")
        return 0

    if not SCHEDULE.exists():
        print(
            f"error: {SCHEDULE.relative_to(REPO).as_posix()} not found - "
            "run `git submodule update --init` (needs access to the solutions repository)",
            file=sys.stderr,
        )
        return 1

    claimed = scheduled()
    if not claimed:
        print(f"error: {SCHEDULE.name} lists no files", file=sys.stderr)
        return 1

    problems = []

    for name in sorted(set(found) | set(claimed)):
        in_material = found.get(name)
        in_schedule = claimed.get(name)

        if in_material is None:
            problems.append(f"{name}: listed in the schedule but the file does not exist")
            continue
        if in_schedule is None:
            problems.append(f"{name}: exists but is not in the schedule")
            continue

        missing = [s for s in in_material if s not in in_schedule]
        extra = [s for s in in_schedule if s not in in_material]
        for s in missing:
            problems.append(f"{name}: section '{s}' is in the material but not the schedule")
        for s in extra:
            problems.append(f"{name}: section '{s}' is in the schedule but not the material")
        if not missing and not extra and in_material != in_schedule:
            problems.append(f"{name}: sections are listed in a different order than they are taught")

    if problems:
        print("detailed_schedule.md is out of sync with the course material:\n", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        print(
            "\nEdit whichever is wrong. If you changed the schedule on purpose, "
            "update the material to match it.",
            file=sys.stderr,
        )
        return 1

    total = sum(len(v) for v in found.values())
    print(f"detailed_schedule.md is in sync: {len(found)} files, {total} sections.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
