"""Download and unpack the day-2 challenge dataset (plate01.nd2).

    pixi run download-challenge-data

The dataset is ~2.2 GB zipped, far too large to commit, so it lives on polybox
and every student fetches it once during setup. This resolves the same short
link that book/setup/download_data.md shows, so the two cannot drift apart:
change the link there and here together.

Idempotent and resumable: an existing plate01.nd2 is left alone, and an
interrupted download continues from where it stopped (polybox honours Range
requests). The zip is deleted after extraction, but zip and unpacked .nd2
(3.5 GB) coexist briefly, so about 6 GB must be free while this runs.
"""

from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

import requests
from tqdm import tqdm

REPO = Path(__file__).resolve().parents[2]
TARGET_DIR = REPO / "data" / "challenge"
ND2 = TARGET_DIR / "plate01.nd2"
ZIP = TARGET_DIR / "plate01.zip"
PART = ZIP.with_suffix(".zip.part")
ND2_PART = ND2.with_suffix(".nd2.part")

#: Keep in sync with the link in book/setup/download_data.md. It redirects to a
#: polybox (Nextcloud) public share; appending /download to the share URL gives
#: the file itself.
SHORT_URL = "https://u.ethz.ch/BgsSv"

CHUNK = 1 << 20


def require_free_space(needed: int, what: str) -> None:
    free = shutil.disk_usage(TARGET_DIR).free
    if free < needed:
        raise SystemExit(
            f"not enough disk space to {what}: need {needed / 1e9:.1f} GB, "
            f"have {free / 1e9:.1f} GB free on the drive holding {TARGET_DIR}"
        )


def resolve_download_url() -> str:
    response = requests.head(SHORT_URL, allow_redirects=True, timeout=60)
    response.raise_for_status()
    return response.url.rstrip("/") + "/download"


def download(url: str) -> None:
    """Stream the archive to PART, resuming if a partial file exists."""
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    done = PART.stat().st_size if PART.exists() else 0
    headers = {"Range": f"bytes={done}-"} if done else {}

    with requests.get(url, headers=headers, stream=True, timeout=120) as response:
        response.raise_for_status()
        if done and response.status_code != 206:
            # Server ignored the Range header: start over.
            done = 0
        remaining = int(response.headers.get("Content-Length", 0))
        total = remaining + done
        require_free_space(remaining, "download the archive")
        mode = "ab" if done else "wb"
        with PART.open(mode) as handle, tqdm(
            total=total or None, initial=done, unit="B", unit_scale=True,
            desc=ZIP.name,
        ) as bar:
            for chunk in response.iter_content(CHUNK):
                handle.write(chunk)
                bar.update(len(chunk))

    PART.rename(ZIP)


def extract() -> None:
    with zipfile.ZipFile(ZIP) as zf:
        members = [m for m in zf.infolist() if Path(m.filename).name == ND2.name]
        if not members:
            raise SystemExit(f"{ZIP.name} does not contain {ND2.name}: {zf.namelist()}")
        member = members[0]
        require_free_space(member.file_size, f"unpack {ND2.name}")
        print(f"extracting {ND2.name} ({member.file_size / 1e9:.1f} GB) ...")
        # Write to a temporary name so an interrupted extraction never leaves a
        # truncated plate01.nd2 that the next run would mistake for a finished one.
        with zf.open(member) as src, ND2_PART.open("wb") as dst:
            shutil.copyfileobj(src, dst, CHUNK)
    ND2_PART.rename(ND2)


def main() -> int:
    if ND2.exists():
        print(f"already present: {ND2.relative_to(REPO)}")
        return 0

    if not ZIP.exists():
        url = resolve_download_url()
        print(f"downloading {url}")
        download(url)

    extract()
    ZIP.unlink()
    print(f"done: {ND2.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
