"""Package reviewed derived evidence; no raw records enter the public site."""

import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "monthly": "https://transtats.bts.gov/OT_Delay/ot_delaycause1.asp",
    "flights": "https://github.com/tidyverse/nycflights13/tree/df98ef215aa8216fe0838a0b8ac5bada646d814c",
    "license": "https://github.com/tidyverse/nycflights13/blob/df98ef215aa8216fe0838a0b8ac5bada646d814c/DESCRIPTION",
    "conformal": "https://arxiv.org/abs/2107.07511",
    "japan": "https://doi.org/10.1016/j.jairtraman.2026.103037",
    "institution": "https://www.hanaoka.tse.ens.isct.ac.jp/paper.html",
}


def digest(path: Path) -> str:
    """Canonical text hash, invariant to checkout line endings on Windows/Linux."""
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def validate(bundle: dict) -> None:
    """Reconcile complete population and every measured queue with frozen reports."""
    audit = bundle["monthly"]["audit"]
    segments = bundle["monthly"]["segments"]
    assert sum(s["records"] for s in segments) == audit["raw_rows"]
    assert sum(s["flights"] for s in segments) == audit["raw_reported_flights"]
    assert (
        sum(s["rate_flights"] or 0 for s in segments)
        == audit["rate_denominator_flights"]
    )
    assert sum(s["delayed"] or 0 for s in segments) == audit["delayed_flights"]
    assert (
        sum(s["missing_count_records"] for s in segments)
        == audit["missing_delay_count_rows"]
    )
    assert sum(s["reconciliation_flag_records"] for s in segments) == len(
        audit["reconciliation_flag_keys"]
    )
    assert len({(s["carrier"], s["airport"]) for s in segments}) == len(segments)
    for metric, expected in audit["rankings"].items():
        ranked = sorted(
            [s for s in segments if s["eligible"]],
            key=lambda s: (
                s[metric] is None,
                -(s[metric] or 0),
                s["carrier"],
                s["airport"],
            ),
        )[:10]
        for actual, saved in zip(ranked, expected, strict=True):
            assert all(actual[k] == v for k, v in saved.items())
    flight = bundle["forecast"]
    queues = flight["capacities"]
    assert queues["source_sha256"] == flight["results"]["source_sha256"]
    for name, grid in queues["models"].items():
        assert grid["20"] == flight["results"]["test"][name]["alerts"]
        previous_hits = 0
        for capacity in (10, 20, 40, 80):
            row = grid[str(capacity)]
            assert row["hits"] + row["false_alerts"] == row["alerts"]
            assert row["hits"] + row["missed_disruptions"] == queues["severe_outcomes"]
            assert row["alerts"] <= capacity * queues["test_days"]
            assert row["hits"] >= previous_hits
            previous_hits = row["hits"]


def export(reports: Path, output: Path) -> dict:
    names = (
        "audit.json",
        "monthly_segments.json",
        "forecast.json",
        "capacities.json",
        "flights.provenance.json",
    )
    saved = {
        name: json.loads((reports / name).read_text(encoding="utf-8")) for name in names
    }
    bundle = {
        "schema_version": 1,
        "sources": SOURCES,
        "monthly": {
            "study_id": "bts-arrival-july-2026-v1",
            "grain": "carrier plus arrival airport; not origin-destination route",
            "period": "July 2026",
            "geography": "US reported arrivals",
            "audit": saved["audit.json"],
            "segments": saved["monthly_segments.json"],
        },
        "forecast": {
            "study_id": "nyc-departure-2013-v1",
            "grain": "flight departing NYC with known departure-delay outcome",
            "results": saved["forecast.json"],
            "capacities": saved["capacities.json"],
            "provenance": saved["flights.provenance.json"],
        },
        "definitions": {
            "delay_rate": "Known 15+ minute delayed arrival counts / flights on the same records",
            "delay_minutes": "Available reported delayed-arrival minutes; unknown burden is not zero",
            "screen": "100 reported flights per segment; a screen, not statistical confidence",
            "reconciliation": "Flags exceed 0.05 prorated flights or 1 minute; provisional tolerances",
            "mae": "Average absolute difference between prediction and outcome, in minutes; lower is better",
            "severe": "Known departure delay at least 60 minutes",
            "queue": "Top scores per eligible day; deterministic schedule-key ties; no live inference",
            "coverage": "Fraction of known outcomes inside the selected median baseline interval",
        },
        "limitations": [
            "Separate studies: 2026 arrival aggregates are not forecast by the 2013 departure model.",
            "BTS local acquisition history partly verified; derived findings only, raw redistribution rights not established.",
            "Unknown departure outcomes excluded; cancellation performance is not measured.",
            "Schedule availability is assumed; no authenticated decision-time snapshots.",
            "Median baseline ties form an arbitrary deterministic control, not an airline policy or random comparator.",
            "Forest lost validation MAE; test queue findings do not reverse model selection.",
            "90% nominal intervals undercovered on test; no temporal or flight-level reliability guarantee.",
            "No operational adoption, prospective validation, causal delay reduction, fuel savings or NABLA affiliation.",
        ],
    }
    validate(bundle)
    output.mkdir(parents=True, exist_ok=True)
    (output / "evidence.json").write_text(
        json.dumps(bundle, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    with (output / "evidence.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(bundle["monthly"]["segments"][0])
        )
        writer.writeheader()
        writer.writerows(bundle["monthly"]["segments"])
    revision = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    manifest = {
        "schema_version": 1,
        "hash_encoding": "SHA256 of UTF-8 text bytes with CRLF normalized to LF; raw source hashes in reports remain byte hashes",
        "scope": "Derived monthly aggregates and measured frozen historical experiment only; no raw/private data",
        "base_git_revision": revision,
        "revision_note": "Base checkout revision at export; exact generating code is identified by hashes below.",
        "inputs": {name: digest(reports / name) for name in names},
        "generators": {
            name: digest(ROOT / name)
            for name in (
                "aviation_audit.py",
                "flight_research.py",
                "scripts/export_public.py",
            )
        },
        "assets": {
            name: digest(output / name) for name in ("evidence.json", "evidence.csv")
        },
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return bundle


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reports", type=Path, default=ROOT / "reports")
    parser.add_argument("--output", type=Path, default=ROOT / "site")
    args = parser.parse_args()
    export(args.reports, args.output)
    print("Public evidence exported and reconciled with frozen reports.")
