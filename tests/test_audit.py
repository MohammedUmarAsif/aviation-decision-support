import csv
from pathlib import Path

import pytest

from aviation_audit import analyse


def source_file(tmp_path: Path, rows: list[dict]) -> Path:
    base = {
        "year": 2026,
        "month": 7,
        "carrier": "AA",
        "airport": "AAA",
        "arr_flights": 100,
        "arr_del15": 10,
        "arr_delay": 100,
        "carrier_ct": 10,
        "weather_ct": 0,
        "nas_ct": 0,
        "security_ct": 0,
        "late_aircraft_ct": 0,
        "carrier_delay": 100,
        "weather_delay": 0,
        "nas_delay": 0,
        "security_delay": 0,
        "late_aircraft_delay": 0,
        "arr_cancelled": 0,
        "arr_diverted": 0,
    }
    path = tmp_path / "input.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(base))
        writer.writeheader()
        writer.writerows(base | row for row in rows)
    return path


def test_weighted_rate_and_idempotence(tmp_path):
    source = source_file(
        tmp_path, [{}, {"airport": "BBB", "arr_flights": 900, "arr_del15": 450}]
    )
    first = analyse(source, tmp_path / "out")
    assert first["weighted_delay_rate"] == pytest.approx(0.46)
    assert analyse(source, tmp_path / "out") == first


def test_missing_is_not_zero(tmp_path):
    source = source_file(tmp_path, [{}, {"airport": "BBB", "arr_del15": ""}])
    result = analyse(source, tmp_path / "out")
    assert result["missing_delay_count_rows"] == 1
    assert result["rate_denominator_flights"] == 100
    assert result["weighted_delay_rate"] == pytest.approx(0.1)


@pytest.mark.parametrize("rows", [[{}, {}], [{"arr_del15": 101}], [{"month": 13}]])
def test_invalid_input_fails_without_report(tmp_path, rows):
    with pytest.raises(ValueError):
        analyse(source_file(tmp_path, rows), tmp_path / "out")
    assert not (tmp_path / "out").exists()


def test_zero_denominator_is_undefined(tmp_path):
    result = analyse(
        source_file(tmp_path, [{"arr_flights": 0, "arr_del15": 0}]), tmp_path / "out"
    )
    assert result["weighted_delay_rate"] is None


def test_cause_mismatch_is_retained_as_flag(tmp_path):
    result = analyse(source_file(tmp_path, [{"arr_delay": 150}]), tmp_path / "out")
    assert result["cause_minutes_mismatch_rows"] == 1
    assert result["weighted_delay_rate"] == pytest.approx(0.1)


@pytest.mark.parametrize(
    "row",
    [
        {"carrier_ct": -1},
        {"arr_flights": 1.5},
        {"weather_delay": "inf"},
        {"carrier": " "},
        {"arr_cancelled": 101},
    ],
)
def test_extra_invalid_fields(tmp_path, row):
    with pytest.raises(ValueError):
        analyse(source_file(tmp_path, [row]), tmp_path / "out")


def test_missing_causes_are_not_reconciled(tmp_path):
    result = analyse(source_file(tmp_path, [{"weather_ct": ""}]), tmp_path / "out")
    assert result["incomplete_cause_rows"] == 1
    assert result["missing_by_column"]["weather_ct"] == 1


def test_missing_count_does_not_discard_known_burden(tmp_path):
    result = analyse(
        source_file(tmp_path, [{"arr_del15": "", "arr_delay": 1000}]), tmp_path / "out"
    )
    assert result["rankings"]["delay_minutes"][0]["delay_minutes"] == 1000
    assert result["weighted_delay_rate"] is None


def test_unknown_burden_is_not_zero(tmp_path):
    result = analyse(source_file(tmp_path, [{"arr_delay": ""}]), tmp_path / "out")
    assert result["rankings"]["delay_minutes"][0]["delay_minutes"] is None
    assert "unknown" in (tmp_path / "out" / "report.md").read_text(encoding="utf-8")


def test_empty_dataset_rejected(tmp_path):
    with pytest.raises(ValueError, match="Empty"):
        analyse(source_file(tmp_path, []), tmp_path / "out")
