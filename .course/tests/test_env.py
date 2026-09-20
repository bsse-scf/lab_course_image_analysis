"""Environment and data smoke tests.

Run with ``pixi run test``. These are deliberately fast and boring: their job is
to fail in CI rather than in front of twenty students on the morning of day 1.
"""

import hashlib
import re
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "notebooks"))


# --- the stack students actually import in the notebooks ------------------

@pytest.mark.parametrize(
    "module",
    [
        "numpy",
        "scipy",
        "skimage",
        "sklearn",
        "pandas",
        "matplotlib",
        "seaborn",
        "tifffile",
        "nd2",
        "stackview",
        "napari",
        "cellpose",
        "iaf",
    ],
)
def test_import(module):
    __import__(module)


def test_iaf_functions_used_by_the_course_exist():
    """The homework and challenge notebooks depend on these by name."""
    import iaf.fit.models
    import iaf.reg
    import iaf.stats

    assert callable(iaf.reg.multi_image_alignment)
    assert callable(iaf.stats.prepare_histogram)
    assert callable(iaf.fit.models.exponential_model)


def test_course_helper_resolves_data_dir():
    from course import DATA, REPO as COURSE_REPO

    assert COURSE_REPO == REPO
    assert DATA == REPO / "data"


# --- data integrity -------------------------------------------------------

MANIFEST = REPO / "data" / "MANIFEST.md"

# Rows look like: | path | source | accession | license | transform | sha256 |
_ROW = re.compile(r"^\|\s*`(?P<path>[^`]+)`\s*\|.*\|\s*(?P<sha>[0-9a-f]{64})\s*\|\s*$")


def _manifest_rows():
    if not MANIFEST.exists():
        return []
    rows = []
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        match = _ROW.match(line.strip())
        if match:
            rows.append((match["path"], match["sha"]))
    return rows


@pytest.mark.skipif(not MANIFEST.exists(), reason="data/MANIFEST.md not generated yet")
def test_manifest_is_not_empty():
    assert _manifest_rows(), "MANIFEST.md exists but lists no data files"


@pytest.mark.parametrize("relpath,expected_sha", _manifest_rows())
def test_data_file_matches_manifest(relpath, expected_sha):
    """Every file named in the manifest is present and uncorrupted.

    Data is committed as ordinary git blobs, so a missing file here means the
    clone is incomplete or a file was deleted - not an LFS problem.
    """
    path = REPO / relpath
    assert path.exists(), f"{relpath} is missing from the working tree"

    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    assert digest == expected_sha, f"{relpath} does not match its manifest checksum"


# --- size limit ------------------------------------------------------------

IMAGE_SUFFIXES = {".tif", ".tiff", ".png", ".gif"}

#: `data/fiji/` holds the Fiji exercise images and the screenshots of the Fiji
#: manual. Those are opened in Fiji or shown on the site at their native size,
#: so the limit does not apply to them; it guards the Python-track data only.
EXEMPT_DIRS = {"fiji", "_cache"}

DATA_IMAGES = sorted(
    p for p in (REPO / "data").rglob("*")
    if p.is_file()
    and p.suffix.lower() in IMAGE_SUFFIXES
    and not EXEMPT_DIRS & set(p.relative_to(REPO / "data").parts)
)


@pytest.mark.parametrize(
    "path", DATA_IMAGES, ids=[str(p.relative_to(REPO / "data")) for p in DATA_IMAGES]
)
def test_image_within_size_limit(path):
    """No Python-track image in data/ may exceed 512 px on its longest edge.

    The repository stores data as ordinary git blobs - there is no git-lfs - so
    this limit is the only thing keeping a clone small.
    """
    import tifffile
    from imageio.v3 import imread

    array = tifffile.imread(path) if path.suffix.lower() in {".tif", ".tiff"} else imread(path)
    longest = max(array.shape[:2])
    assert longest <= 512, f"{path.name} is {array.shape[:2]} - exceeds the 512 px limit"
