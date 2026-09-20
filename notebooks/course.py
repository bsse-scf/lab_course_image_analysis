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

__all__ = ["REPO", "DATA", "show"]

#: Repository root.
REPO = Path(__file__).resolve().parents[1]

#: Course data directory.
DATA = REPO / "data"

def show(image, title=None, cmap="gray", ax=None, **kwargs):
    """Display a 2D image without axis ticks.

    This function calls ``plt.imshow`` with a grayscale colour map by default.
    Extra keyword arguments are passed to ``plt.imshow``.
    """

    # if no axis is provided, create a new figure and axis
    if ax is None:
        _, ax = plt.subplots()

    # display the image with the specified colour map and any additional keyword arguments
    imshow_output = ax.imshow(image, cmap=cmap, **kwargs)

    # set title if provided
    if title is not None:
        ax.set_title(title)

    # remove axis ticks and labels
    ax.set_axis_off()

    return imshow_output
