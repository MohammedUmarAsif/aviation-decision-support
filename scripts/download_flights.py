"""Download a pinned CC0 teaching dataset; preserve RDA and record conversion hashes."""

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from urllib.request import urlopen

import pyreadr

COMMIT = "df98ef215aa8216fe0838a0b8ac5bada646d814c"
URL = f"https://raw.githubusercontent.com/tidyverse/nycflights13/{COMMIT}/data/flights.rda"


def download(root: Path = Path("data/raw")) -> None:
    root.mkdir(parents=True, exist_ok=True)
    rda = root / "flights.rda"
    with urlopen(URL, timeout=60) as response:
        payload = response.read(50_000_001)
    if len(payload) > 50_000_000:
        raise ValueError("Unexpected download size")
    rda.write_bytes(payload)
    frame = pyreadr.read_r(str(rda))["flights"]
    csv = root / "flights.csv"
    frame.to_csv(csv, index=False, lineterminator="\n")
    manifest = {
        "url": URL,
        "commit": COMMIT,
        "retrieved_at_utc": datetime.now(UTC).isoformat(),
        "license": "CC0 (upstream DESCRIPTION)",
        "rda_sha256": hashlib.sha256(payload).hexdigest(),
        "csv_sha256": hashlib.sha256(csv.read_bytes()).hexdigest(),
        "rows": len(frame),
        "conversion": "pyreadr to pandas CSV; versions pinned in uv.lock",
    }
    (root / "flights.provenance.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    download()
