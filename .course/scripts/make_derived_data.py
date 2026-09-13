"""Generate the derived images used by the Fiji exercises.

These are not downloaded - they are made from data already in the repository, so
that the exercises have material with a *known* right answer. Deterministic:
re-running produces byte-identical output.

    pixi run make-derived

Run `pixi run fetch-data` afterwards to refresh data/MANIFEST.md.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import tifffile
from scipy.ndimage import shift as ndshift
from skimage.filters import gaussian
from skimage.util import random_noise

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "data"

#: Offsets applied to build the registration exercise, in (row, col) pixels.
#: These are the answer key - see book/fiji/e2_registration.md.
REG_OFFSETS = {
    "channel2": (-11, 7),
    "channel3": (6, -13),
}


def build_registration() -> list[Path]:
    """A three-channel set with two channels deliberately shifted.

    The homework asks students to register DAPI/GFP/Cy3 triplets acquired on a
    hand-built microscope. That data does not exist until they acquire it, so
    this stands in for it: same task, known answer.

    All three channels are built from the *same* source image, then processed to
    look different (blurred and dimmed, or noisy and brighter). That matters: if
    the channels held genuinely different stains, the "correct" shift would not
    be well defined and students could not check their answer against the key.
    Registering different stains is the harder, real case - that is the homework.
    """
    out = DATA / "fiji" / "registration"
    out.mkdir(parents=True, exist_ok=True)

    source = tifffile.imread(DATA / "bbbc020" / "images" / "15min_3_nuclei.tif")
    rng = np.random.default_rng(20260909)

    # Same underlying structure, different appearance.
    dim_blurred = gaussian(source, sigma=1.5, preserve_range=True) * 0.6
    noisy_bright = np.clip(source.astype(float) * 1.4 + rng.normal(0, 6, source.shape), 0, 255)

    written = []
    for name, image, offset in (
        ("channel1_reference", source.astype(float), (0, 0)),
        ("channel2", dim_blurred, REG_OFFSETS["channel2"]),
        ("channel3", noisy_bright, REG_OFFSETS["channel3"]),
    ):
        moved = ndshift(image, offset, order=1, mode="constant", cval=0)
        path = out / f"{name}.tif"
        tifffile.imwrite(path, np.clip(moved, 0, 255).astype(np.uint8), compression="deflate")
        written.append(path)
    return written


def build_artifacts() -> list[Path]:
    """Three processed copies of one image, for 'spot the artifact'.

    Each has had exactly one thing done to it. The answer key lives in
    .course/solutions/instructor_notes.md, not here.
    """
    out = DATA / "misc" / "artifacts"
    out.mkdir(parents=True, exist_ok=True)

    source = tifffile.imread(DATA / "bbbc020" / "images" / "Kontrolle2_nuclei.tif")
    rng = np.random.default_rng(20260909)

    variants = {
        # A: over-smoothed - detail destroyed by too large a Gaussian.
        "sample_a": gaussian(source, sigma=4, preserve_range=True),
        # B: saturated - brightness pushed until bright nuclei clip to 255.
        "sample_b": np.clip(source.astype(float) * 2.6, 0, 255),
        # C: salt-and-pepper noise, as from a failing detector.
        "sample_c": random_noise(source, mode="s&p", amount=0.04, rng=rng) * 255,
    }

    written = []
    for name, array in variants.items():
        path = out / f"{name}.tif"
        tifffile.imwrite(path, array.astype(np.uint8), compression="deflate")
        written.append(path)

    tifffile.imwrite(out / "unmodified.tif", source, compression="deflate")
    written.append(out / "unmodified.tif")
    return written


def main() -> int:
    written = build_registration() + build_artifacts()
    for path in written:
        print(f"  wrote {path.relative_to(REPO)}")
    print(f"\n{len(written)} files. Run `pixi run fetch-data` to refresh the manifest.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
