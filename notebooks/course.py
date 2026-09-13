"""Small helpers shared by all course notebooks.

Import this at the top of a notebook to get a reliable path to the data::

    from course import DATA, show

    nuclei = tifffile.imread(DATA / "bbbc020" / "images" / "jw-1h_1_dapi.tif")
    show(nuclei)

`DATA` is resolved from this file's own location, so it points at the right
place no matter which directory JupyterLab, VSCode or pytest happened to start
in. Prefer it over a relative path like ``"../data/..."``.
"""

from pathlib import Path

import matplotlib.pyplot as plt

__all__ = ["REPO", "DATA", "show", "CHALLENGE_URL", "download_challenge_data"]

#: Repository root.
REPO = Path(__file__).resolve().parents[1]

#: Course data directory.
DATA = REPO / "data"

#: Polybox share holding the day-2 challenge dataset (plate01, ~3.3 GB).
#: Carried over from the previous edition - re-check it still resolves before
#: the course starts; the weekly link check in CI covers it during the year.
CHALLENGE_URL = "https://polybox.ethz.ch/index.php/s/opKPgFNikwfg8AL"


def show(image, title=None, cmap="gray", ax=None, **kwargs):
    """Display a 2D image with sensible defaults and no axis ticks.

    A thin wrapper around ``plt.imshow`` - it exists so notebooks can show an
    image in one short line without repeating the same four styling arguments
    every time. Extra keyword arguments are passed straight through.
    """
    if ax is None:
        _, ax = plt.subplots()
    handle = ax.imshow(image, cmap=cmap, **kwargs)
    if title is not None:
        ax.set_title(title)
    ax.set_axis_off()
    return handle


def download_challenge_data():
    """Explain how to obtain the day-2 challenge dataset.

    The file is ~3.3 GB, which is far too large to track in the repository, so
    it is not downloaded automatically: on a lecture-room network that decision
    belongs to you, not to a notebook cell. Most of the challenge can be done
    without it - see the two tracks described in ``book/challenge.md``.
    """
    target = DATA / "challenge" / "plate01.nd2"
    if target.exists():
        print(f"Challenge data already present: {target}")
        return target

    print(
        "The challenge dataset (plate01, ~3.3 GB) is not in the repository.\n"
        f"\n  1. Download it from: {CHALLENGE_URL}"
        f"\n  2. Extract it and place plate01.nd2 at:\n     {target}\n"
        "\nYou do not need it to complete the analysis half of the challenge: "
        "ask the instructors for plate01_summary.csv, which holds the per-field "
        "counts (see book/challenge.md, Track B)."
    )
    return None
