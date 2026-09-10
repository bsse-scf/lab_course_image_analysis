"""Download, subset and normalise the BBBC datasets used by the course.

Instructor-only and idempotent. Students never run this - they get the results
by cloning, because everything it writes is committed via git-lfs.

    pixi run fetch-data                 # build every dataset
    pixi run fetch-data --set bbbc020   # just one
    pixi run fetch-data --verify        # re-check emitted files against MANIFEST.md

Every archive layout below was verified by inspection rather than taken from the
BBBC pages, which do not document them. The quirks are real and each one is
commented where it is handled.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import sys
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import tifffile
from imageio.v3 import imread as imread_png
from scipy.ndimage import binary_fill_holes
from skimage.measure import label as label_components
from skimage.segmentation import relabel_sequential

sys.path.insert(0, str(Path(__file__).resolve().parent))
from downscale import check_labels_survived, downscale_image, downscale_labels

REPO = Path(__file__).resolve().parents[1]
DATA = REPO / "data"
CACHE = DATA / "_cache"
MANIFEST = DATA / "MANIFEST.md"

BASE = "https://data.broadinstitute.org/bbbc"

# Junk that Windows and macOS left inside the published archives.
JUNK = re.compile(r"(^|/)(__MACOSX/|\._|Thumbs\.db$)")


@dataclass
class Archive:
    name: str
    url: str
    sha256: str


@dataclass
class Dataset:
    name: str
    title: str
    page: str
    licence: str
    archives: list[Archive]
    builder: str
    notes: str = ""
    fields: list[str] = field(default_factory=list)
    #: Pixels to trim from every edge, at the SOURCE resolution, before
    #: downscaling. See CROPPING below for why this is not zero.
    crop_margin: int = 0


# --------------------------------------------------------------------------
# Dataset declarations
# --------------------------------------------------------------------------

DATASETS: dict[str, Dataset] = {
    "bbbc020": Dataset(
        name="bbbc020",
        title="Murine bone-marrow derived macrophages",
        page="https://bbbc.broadinstitute.org/BBBC020",
        licence="CC BY 3.0 - Broad Bioimage Benchmark Collection",
        builder="build_bbbc020",
        crop_margin=150,   # median annotated cell diameter is ~147 px here
        # Controls are spelled "Kontrolle" in the source data; schedule.md's
        # "control 1, 2, 3" means these three.
        fields=[
            "jw-Kontrolle1", "jw-Kontrolle2", "jw-Kontrolle3",
            "jw-15min 1", "jw-15min 2", "jw-15min 3",
            "jw-1h 1", "jw-1h 2",
            "jw-2h 1", "jw-2h 2",
            "jw-24h 1", "jw-24h 2",
        ],
        # Ground truth covers only 20 of the 25 field sets - the whole "30min"
        # series is unannotated - so every field here is one that has both
        # nuclei and cell outlines.
        notes=(
            "Source images are 1040x1388 RGB uint8 with a false-colour LUT baked in "
            "(c1/cells in R+G, c5/nuclei in B); intensity recovered as max over the "
            "channel axis. Ground truth ships as one binary TIFF per object and is "
            "merged here into a single uint16 label image per field."
        ),
        archives=[
            Archive("images", f"{BASE}/BBBC020/BBBC020_v1_images.zip",
                    "edf4a87be957ec2b7ab268bef92c2efae8e098dc0855a4fa9df80895ff7062e4"),
            Archive("outlines_nuclei", f"{BASE}/BBBC020/BBBC020_v1_outlines_nuclei.zip",
                    "b212f10013ae2a0260976cff2134204ecba226853922aea2ab5289051a47ceb7"),
            Archive("outlines_cells", f"{BASE}/BBBC020/BBBC020_v1_outlines_cells.zip",
                    "6f65b05eb5d5c52829004760a01a93c07863676547605516b6e5fce47f8516d5"),
        ],
    ),
    "bbbc010": Dataset(
        name="bbbc010",
        title="C. elegans live/dead assay",
        page="https://bbbc.broadinstitute.org/BBBC010",
        licence="CC BY 3.0 - Broad Bioimage Benchmark Collection",
        builder="build_bbbc010",
        crop_margin=105,   # median worm extent is ~104 px here
        # Columns 1-12 are ampicillin (mostly dead, rod-shaped), 13-24 untreated
        # (live, curled). Take some of each so the detective game has both.
        fields=["A22", "B22", "C14", "D17", "A09", "B09", "C09", "D09"],
        notes=(
            "520x696 uint16, two channels per well (w1 GFP, w2 brightfield). Images sit "
            "flat in the archive with a UUID suffix; ground truth is one binary PNG per "
            "worm, merged here into a uint16 label image per well."
        ),
        archives=[
            Archive("images", f"{BASE}/BBBC010/BBBC010_v2_images.zip",
                    "77a82c74d12c0707e861d9b324b47e6a74e316aefe25a3501f596c7a80a0b4f4"),
            Archive("foreground", f"{BASE}/BBBC010/BBBC010_v1_foreground_eachworm.zip",
                    "19b7ceef05d4a21bb3eec9988ee0b61dd0eeb940fb690125f14bb5919ae8ae44"),
        ],
    ),
    "bbbc030": Dataset(
        name="bbbc030",
        title="Chinese hamster ovary cells (DIC)",
        page="https://bbbc.broadinstitute.org/BBBC030",
        licence="CC BY 3.0 - Broad Bioimage Benchmark Collection",
        builder="build_bbbc030",
        crop_margin=60,    # median cell extent is ~59 px here
        fields=[f"cho{i:02d}" for i in range(1, 9)],
        notes=(
            "1032x1376 RGB uint8 DIC. Ground truth ships as cell OUTLINES, not filled "
            "masks, so it is hole-filled and connected-component labelled here; stray "
            "components under 500 px are dropped."
        ),
        archives=[
            Archive("images", f"{BASE}/BBBC030/images.zip",
                    "a6c3e4e5b22e959aef2d003d4b2112e18cdc45116af9ec49dd827b26d7c3df0c"),
            Archive("ground_truth", f"{BASE}/BBBC030/ground_truth.zip",
                    "6748fa1c0381a5841a1050338ecde6bb6f8a977f38b347352e598757e6da4711"),
        ],
    ),
}


# --------------------------------------------------------------------------
# Download / extract helpers
# --------------------------------------------------------------------------

def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fetch(archive: Archive) -> Path:
    """Download an archive into the cache unless it is already there and valid."""
    CACHE.mkdir(parents=True, exist_ok=True)
    target = CACHE / Path(archive.url).name

    if target.exists() and sha256_of(target) == archive.sha256:
        return target

    import requests

    print(f"  downloading {target.name} ...")
    with requests.get(archive.url, stream=True, timeout=120) as response:
        response.raise_for_status()
        with target.open("wb") as handle:
            for chunk in response.iter_content(1 << 20):
                handle.write(chunk)

    actual = sha256_of(target)
    if actual != archive.sha256:
        raise SystemExit(
            f"checksum mismatch for {target.name}\n  expected {archive.sha256}\n  got      {actual}"
        )
    return target


def extract(archive_path: Path, dest: Path) -> Path:
    """Extract an archive once, skipping the junk the publishers left in it."""
    dest.mkdir(parents=True, exist_ok=True)
    marker = dest / ".extracted"
    if marker.exists():
        return dest

    with zipfile.ZipFile(archive_path) as zf:
        for member in zf.namelist():
            if JUNK.search(member) or member.endswith("/"):
                continue
            zf.extract(member, dest)

    marker.touch()
    return dest


def merge_objects(paths, shape) -> np.ndarray:
    """Merge per-object binary masks into a single uint16 label image.

    Later objects win where masks overlap, which is what the source data implies:
    the per-object files are disjoint apart from a pixel or two of anti-aliasing.
    """
    labels = np.zeros(shape, dtype=np.uint16)
    for index, path in enumerate(sorted(paths), start=1):
        mask = imread_png(path) if path.suffix.lower() == ".png" else tifffile.imread(path)
        if mask.ndim == 3:
            mask = mask.max(axis=-1)
        labels[mask > 127] = index
    return labels


# ---------------------------------------------------------------------------
# CROPPING
#
# All three BBBC sets annotate only objects that do NOT touch the image border:
# 0% of BBBC010 worms, 1% of BBBC030 cells and 5% of BBBC020 cells sit on an
# edge, while the images plainly contain objects there. On BBBC020 roughly a
# quarter of the outer band is stained tissue and only 8% of it is annotated.
#
# Scoring a segmentation against that is unfair in a specific, confusing way: a
# method is penalised for correctly finding the very objects the annotator chose
# to skip, and the penalty lands entirely in false positives. Since day 2 is
# built on comparing methods against this ground truth, every image is trimmed
# by roughly one typical object diameter first, which removes the unannotated
# band. Objects the crop bisects are cut in the image and the annotation alike,
# so the two stay consistent.
# ---------------------------------------------------------------------------

#: Longest edge of any image committed to the repository. Data is stored as
#: ordinary git blobs (no git-lfs), so keeping it small is what keeps clones
#: fast - see AGENTS.md.
MAX_SIZE = 512


def crop_border(array: np.ndarray, margin: int) -> np.ndarray:
    """Trim `margin` pixels from every edge."""
    if not margin:
        return array
    return array[margin:-margin, margin:-margin]


def save_image(path: Path, array: np.ndarray, margin: int = 0) -> None:
    """Crop the border, downscale, and write."""
    path.parent.mkdir(parents=True, exist_ok=True)
    cropped = crop_border(array, margin)
    tifffile.imwrite(path, downscale_image(cropped, MAX_SIZE), compression="deflate")


def save_labels(path: Path, array: np.ndarray, margin: int = 0) -> None:
    """Downscale a label image and write it, warning if any object was lost.

    Nearest-neighbour resizing can drop an object small enough to fall between
    the new pixel centres. That would silently corrupt the day-2 metrics
    exercise, so it is reported rather than swallowed.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    cropped = crop_border(array, margin)
    # Objects removed entirely by the crop leave gaps in the numbering, so
    # renumber - otherwise labels.max() overcounts.
    cropped, _, _ = relabel_sequential(cropped)
    small = downscale_labels(cropped, MAX_SIZE)
    lost = check_labels_survived(cropped, small)
    if lost:
        print(f"    ! {path.name}: lost {len(lost)} object(s) when downscaling: {lost}",
              file=sys.stderr)
    tifffile.imwrite(path, small, compression="deflate")


# --------------------------------------------------------------------------
# Per-dataset builders
# --------------------------------------------------------------------------

def build_bbbc020(ds: Dataset, roots: dict[str, Path]) -> list[Path]:
    written: list[Path] = []
    images = roots["images"] / "BBBC020_v1_images"
    # NOTE: the outline archives spell the directory "BBC020" - one B short.
    # Glob for it rather than hardcoding either spelling.
    nuclei_root = next(roots["outlines_nuclei"].glob("BB*_v1_outlines_nuclei"))
    cells_root = next(roots["outlines_cells"].glob("BB*_v1_outlines_cells"))

    for fieldname in ds.fields:
        slug = fieldname.replace(" ", "_").replace("jw-", "")

        # c5 is the blue DAPI channel (nuclei); c1 is CD11b/APC on the cell
        # surface. Verified rather than assumed: with this pairing an Otsu
        # threshold scores IoU ~0.65-0.72 against the nuclei ground truth and
        # only ~0.25-0.50 against the cells, which is the whole reason the
        # course reaches for Weka on the cell channel. Swapping them scores
        # ~0.08 on both.
        for channel, role in (("c5", "nuclei"), ("c1", "cells")):
            source = images / fieldname / f"{fieldname}_{channel}.TIF"
            if not source.exists():
                print(f"    ! missing {source.name}", file=sys.stderr)
                continue
            rgb = tifffile.imread(source)
            # False-colour LUT is baked in; max over channels recovers intensity.
            grey = rgb.max(axis=-1) if rgb.ndim == 3 else rgb
            out = DATA / ds.name / "images" / f"{slug}_{role}.tif"
            save_image(out, grey.astype(np.uint8), ds.crop_margin)
            written.append(out)

        # Ground truth: nuclei objects are named *_c5_N, cells *_c1_N. That looks
        # swapped against the channel naming, but object sizes confirm it.
        for root, pattern, role in (
            (nuclei_root, f"{fieldname}_c5_*.TIF", "nuclei"),
            (cells_root, f"{fieldname}_c1_*.TIF", "cells"),
        ):
            objects = sorted(root.glob(pattern))
            if not objects:
                continue
            shape = tifffile.imread(objects[0]).shape[:2]
            out = DATA / ds.name / "gt" / f"{slug}_{role}_labels.tif"
            save_labels(out, merge_objects(objects, shape), ds.crop_margin)
            written.append(out)

    return written


def build_bbbc010(ds: Dataset, roots: dict[str, Path]) -> list[Path]:
    written: list[Path] = []
    image_root = roots["images"]
    gt_root = roots["foreground"] / "BBBC010_v1_foreground_eachworm"

    for well in ds.fields:
        for channel, role in (("w1", "gfp"), ("w2", "brightfield")):
            # Flat layout with a UUID suffix, so match on the well+channel infix.
            matches = sorted(image_root.glob(f"*_{well}_{channel}_*.tif"))
            if not matches:
                print(f"    ! no image for {well} {channel}", file=sys.stderr)
                continue
            save_image(DATA / ds.name / "images" / f"{well}_{role}.tif", tifffile.imread(matches[0]), ds.crop_margin)
            written.append(DATA / ds.name / "images" / f"{well}_{role}.tif")

        worms = sorted(gt_root.glob(f"{well}_*_ground_truth.png"))
        if worms:
            shape = imread_png(worms[0]).shape[:2]
            out = DATA / ds.name / "gt" / f"{well}_worm_labels.tif"
            save_labels(out, merge_objects(worms, shape), ds.crop_margin)
            written.append(out)

    return written


def build_bbbc030(ds: Dataset, roots: dict[str, Path]) -> list[Path]:
    written: list[Path] = []
    image_root = roots["images"] / "images"
    gt_root = roots["ground_truth"] / "ground_truth"

    for name in ds.fields:
        source = image_root / f"{name}.png"
        if not source.exists():
            print(f"    ! missing {source.name}", file=sys.stderr)
            continue
        rgb = imread_png(source)
        grey = rgb.max(axis=-1) if rgb.ndim == 3 else rgb
        out = DATA / ds.name / "images" / f"{name}_dic.tif"
        save_image(out, grey.astype(np.uint8), ds.crop_margin)
        written.append(out)

        gt_source = gt_root / f"{name}.png"
        if not gt_source.exists():
            continue
        # Outlines, not filled masks - fill before labelling.
        filled = binary_fill_holes(imread_png(gt_source) > 100)
        labels = label_components(filled).astype(np.uint16)
        for index in range(1, labels.max() + 1):
            if (labels == index).sum() < 500:  # anti-aliasing specks
                labels[labels == index] = 0
        out = DATA / ds.name / "gt" / f"{name}_cell_labels.tif"
        save_labels(out, label_components(labels > 0).astype(np.uint16), ds.crop_margin)
        written.append(out)

    return written


BUILDERS = {
    "build_bbbc020": build_bbbc020,
    "build_bbbc010": build_bbbc010,
    "build_bbbc030": build_bbbc030,
}


# --------------------------------------------------------------------------
# Manifest
# --------------------------------------------------------------------------

#: Images that were not downloaded but carried over from earlier editions of the
#: course. They are recorded in the manifest so their checksums are verified too.
MISC_PROVENANCE = {
    "rice.png": "classic test image (uneven illumination); previous course edition",
    "actin.tif": "actin filaments; previous course edition",
    "cells_shaded.tif": "vignetted fluorescence field; previous course edition",
    "timelapse": "7-frame phase-contrast timelapse, 30 min interval; previous course edition",
    "registration": "derived: BBBC020 15min_3 with two channels deliberately shifted (scripts/make_derived_data.py)",
    "artifacts": "derived: BBBC020 Kontrolle2 with one processing artifact each (scripts/make_derived_data.py)",
}


HEADER = """# Data provenance

Generated by `scripts/fetch_data.py` - do not edit by hand.

Every file below is redistributed from the Broad Bioimage Benchmark Collection
under CC BY 3.0, border-cropped (see scripts/fetch_data.py) and downscaled so
the longest edge is at most 512 px.
Cite the dataset page when you use it. `pixi run test` verifies
each checksum, so a corrupt or missing file fails CI instead of failing in class.

"""


def write_manifest(entries: dict[str, list[Path]]) -> None:
    lines = [HEADER]
    for key, paths in entries.items():
        ds = DATASETS[key]
        lines.append(f"## {ds.name.upper()} — {ds.title}\n")
        lines.append(f"- Source: <{ds.page}>")
        lines.append(f"- Licence: {ds.licence}")
        if ds.notes:
            lines.append(f"- Processing: {ds.notes}")
        lines.append("")
        lines.append("| file | source | accession | licence | transform | sha256 |")
        lines.append("|---|---|---|---|---|---|")
        for path in sorted(paths):
            rel = path.relative_to(REPO).as_posix()
            kind = ("label image, merged per-object masks, nearest-neighbour downscaled"
                if "/gt/" in rel else "intensity image, anti-aliased downscaled")
            lines.append(
                f"| `{rel}` | {ds.page} | {ds.name.upper()} | CC BY 3.0 | {kind} | {sha256_of(path)} |"
            )
        lines.append("")
    local = sorted(
        p for d in ("misc", "fiji") for p in (DATA / d).rglob("*") if p.is_file()
    )
    if local:
        lines.append("## Supporting images (not downloaded)\n")
        lines.append(
            "Carried over from earlier editions of this course, or derived from the "
            "datasets above by `scripts/make_derived_data.py`. All at most 512 px on "
            "the longest edge.\n"
        )
        lines.append("| file | source | accession | licence | transform | sha256 |")
        lines.append("|---|---|---|---|---|---|")
        for path in local:
            rel = path.relative_to(REPO).as_posix()
            key = path.name if path.name in MISC_PROVENANCE else path.parent.name
            note = MISC_PROVENANCE.get(key, "previous course edition")
            lines.append(
                f"| `{rel}` | {note} | - | see source | downscaled to <=512 px | {sha256_of(path)} |"
            )
        lines.append("")

    MANIFEST.write_text("\n".join(lines))
    print(f"\nwrote {MANIFEST.relative_to(REPO)}")


def verify() -> int:
    if not MANIFEST.exists():
        print("no MANIFEST.md - run `pixi run fetch-data` first", file=sys.stderr)
        return 1
    row = re.compile(r"^\|\s*`([^`]+)`\s*\|.*\|\s*([0-9a-f]{64})\s*\|\s*$")
    bad = 0
    checked = 0
    for line in MANIFEST.read_text().splitlines():
        match = row.match(line.strip())
        if not match:
            continue
        checked += 1
        path = REPO / match.group(1)
        if not path.exists():
            print(f"MISSING  {match.group(1)}")
            bad += 1
        elif sha256_of(path) != match.group(2):
            print(f"CORRUPT  {match.group(1)}")
            bad += 1
    print(f"{checked - bad}/{checked} files OK")
    return 1 if bad else 0


#: Files under data/ that this script must never touch. The Weka classifier is
#: trained by hand in Fiji over a good half hour and cannot be regenerated by
#: any script, so a careless rebuild of the dataset directory destroys real work.
#: (This guard exists because exactly that happened once.)
PROTECTED = ("weka",)


def guard_protected(dataset: str) -> None:
    """Warn loudly if irreplaceable hand-made files are missing."""
    weka = DATA / dataset / "weka"
    model = weka / f"{dataset}_cells.model"
    if weka.exists() and not model.exists():
        print(
            f"  ! {model.relative_to(REPO)} is missing.\n"
            f"    It is trained by hand in Fiji and cannot be scripted - see\n"
            f"    {weka.relative_to(REPO)}/README.md",
            file=sys.stderr,
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--set", dest="only", choices=sorted(DATASETS), help="build one dataset")
    parser.add_argument("--verify", action="store_true", help="check emitted files against MANIFEST.md")
    parser.add_argument("--keep-cache", action="store_true", help="keep extracted archives in data/_cache")
    args = parser.parse_args()

    if args.verify:
        return verify()

    selected = [args.only] if args.only else list(DATASETS)
    entries: dict[str, list[Path]] = {}

    for key in selected:
        ds = DATASETS[key]
        print(f"\n{ds.name}: {ds.title}")
        roots = {}
        for archive in ds.archives:
            path = fetch(archive)
            roots[archive.name] = extract(path, CACHE / f"{ds.name}_{archive.name}")
        written = BUILDERS[ds.builder](ds, roots)
        guard_protected(ds.name)
        print(f"  wrote {len(written)} files to data/{ds.name}/")
        entries[key] = written

    # Merge with any datasets that were not rebuilt this run.
    if args.only and MANIFEST.exists():
        for key in DATASETS:
            if key in entries:
                continue
            existing = sorted((DATA / key).rglob("*.tif"))
            if existing:
                entries[key] = existing

    write_manifest({k: entries[k] for k in DATASETS if k in entries})

    if not args.keep_cache:
        for path in CACHE.glob("*_*"):
            if path.is_dir():
                shutil.rmtree(path, ignore_errors=True)
        print("cleaned extracted archives (zips kept; --keep-cache to keep both)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
