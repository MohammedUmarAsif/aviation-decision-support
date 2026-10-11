"""Check public population, unknown-value handling and frozen queue accounting."""

import json
from pathlib import Path

import numpy as np
import pytest
from test_audit import source_file
from test_research import flights

from aviation_audit import analyse
from flight_research import alert_metrics
from scripts.export_public import ROOT, digest, export, validate


def test_complete_segments_include_small_and_unknown(tmp_path):
    source = source_file(
        tmp_path,
        [{}, {"airport": "BBB", "arr_flights": 1, "arr_del15": "", "arr_delay": ""}],
    )
    analyse(source, tmp_path / "out")
    segments = json.loads((tmp_path / "out/monthly_segments.json").read_text())
    assert len(segments) == 2
    small = segments[1]
    assert small["eligible"] is False
    assert small["delayed"] is None and small["rate_flights"] is None
    assert small["delay_rate"] is None and small["delay_minutes"] is None
    assert small["missing_count_records"] == small["missing_burden_records"] == 1


def test_complete_export_preserves_burden_without_known_count(tmp_path):
    source = source_file(tmp_path, [{"arr_del15": ""}])
    analyse(source, tmp_path / "out")
    row = json.loads((tmp_path / "out/monthly_segments.json").read_text())[0]
    assert row["delay_minutes"] == 100
    assert row["delay_rate"] is None


def test_capacity_grid_accounting_and_daily_clipping():
    frame = flights().iloc[:4].copy()
    frame["date"] = "2013-11-01"
    scores = np.ones(len(frame))
    for capacity in (1, 2, 10, 20, 40, 80):
        row = alert_metrics(frame, scores, capacity)
        assert row["alerts"] == min(capacity, 4)
        assert row["hits"] + row["false_alerts"] == row["alerts"]
        assert row["hits"] + row["missed_disruptions"] == 1


def test_public_bundle_and_manifest(tmp_path):
    bundle = export(ROOT / "reports", tmp_path)
    validate(bundle)
    manifest = json.loads((tmp_path / "manifest.json").read_text())
    for asset, expected in manifest["assets"].items():
        assert digest(tmp_path / asset) == expected
    assert (
        bundle["forecast"]["capacities"]["models"]["train_median"]["20"]["hits"] == 120
    )
    assert (
        bundle["forecast"]["capacities"]["models"]["random_forest"]["20"]["hits"] == 239
    )
    assert bundle["monthly"]["audit"]["raw_reported_flights"] == 697754


def test_public_validation_rejects_reconstructed_or_inconsistent_data():
    bundle = json.loads((ROOT / "site/evidence.json").read_text())
    bundle["monthly"]["segments"] = bundle["monthly"]["segments"][:10]
    with pytest.raises(AssertionError):
        validate(bundle)


def test_committed_assets_and_generators_match_manifest():
    manifest = json.loads((ROOT / "site/manifest.json").read_text())
    for section, directory in (
        ("assets", "site"),
        ("inputs", "reports"),
        ("generators", "."),
    ):
        for name, expected in manifest[section].items():
            assert digest(ROOT / directory / Path(name)) == expected
