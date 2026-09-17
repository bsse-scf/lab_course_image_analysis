"""Small helpers shared by all course notebooks.

Import this at the top of a notebook to get a reliable path to the data::

    from course import DATA, show

    nuclei = tifffile.imread(DATA / "bbbc020" / "images" / "2h_1_nuclei.tif")
    show(nuclei)

The variable `DATA` is defined based on this file's location, so it also works when JupyterLab
starts in a different directory. Use it instead of a relative data path.
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
    """Display a 2D image without axis ticks.

    This wrapper calls ``plt.imshow`` with a grayscale colour map by default.
    Extra keyword arguments are passed to ``plt.imshow``.
    """
    if ax is None:
        _, ax = plt.subplots()
    handle = ax.imshow(image, cmap=cmap, **kwargs)
    if title is not None:
        ax.set_title(title)
    ax.set_axis_off()
    return handle
