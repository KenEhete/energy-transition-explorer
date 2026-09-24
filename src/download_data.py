"""
Step 1: download the raw data and record what was downloaded.

Why a manifest? Our World in Data updates these files regularly,
so numbers can change between downloads. The manifest stores the
download time, file size and a SHA-256 checksum for each file.
If your results ever shift, you can tell whether the data changed.

Run from the project root:
    python -m src.download_data
"""
import hashlib
import json
from datetime import datetime, timezone

import requests

from src.config import DATA_RAW, MANIFEST, SOURCES


def sha256_of(path) -> str:
    """Return the SHA-256 checksum of a file (its 'fingerprint')."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download(filename: str, url: str) -> dict:
    """Download one file into data/raw and return its manifest entry."""
    target = DATA_RAW / filename
    print(f"Downloading {filename} ...")
    response = requests.get(url, timeout=120)
    response.raise_for_status()  # stop loudly if the download fails
    target.write_bytes(response.content)

    return {
        "file": filename,
        "url": url,
        "bytes": target.stat().st_size,
        "sha256": sha256_of(target),
    }


def main() -> None:
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    entries = [download(name, url) for name, url in SOURCES.items()]

    manifest = {
        "downloaded_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "files": entries,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2))
    print(f"\nDone. Manifest written to {MANIFEST}")


if __name__ == "__main__":
    main()
