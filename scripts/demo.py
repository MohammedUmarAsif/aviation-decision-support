"""Offline diagnostic demonstration using clearly synthetic data."""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from aviation_audit import analyse  # noqa: E402


def demo() -> None:
    path = Path("data/synthetic/monthly.csv")
    path.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "year": 2026,
        "month": 7,
        "carrier": "EX",
        "airport": "AAA",
        "arr_flights": 100,
        "arr_del15": 20,
        "arr_delay": 1200,
        "carrier_ct": 20,
        "weather_ct": 0,
        "nas_ct": 0,
        "security_ct": 0,
        "late_aircraft_ct": 0,
        "carrier_delay": 1200,
        "weather_delay": 0,
        "nas_delay": 0,
        "security_delay": 0,
        "late_aircraft_delay": 0,
        "arr_cancelled": 0,
        "arr_diverted": 0,
    }
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        writer.writeheader()
        writer.writerow(row)
        writer.writerow(
            row
            | {
                "airport": "BBB",
                "arr_flights": 1000,
                "arr_del15": 100,
                "carrier_ct": 100,
                "arr_delay": 6000,
                "carrier_delay": 6000,
            }
        )
    result = analyse(path, Path("reports/demo"))
    assert result["weighted_delay_rate"] == 120 / 1100
    print(
        "Synthetic demo passed. Read reports/demo/report.md; this is not observed airline evidence."
    )


if __name__ == "__main__":
    demo()
