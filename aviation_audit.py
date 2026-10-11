"""Reproducible audit and descriptive analysis of BTS monthly delay data."""

import argparse
import hashlib
import json
from pathlib import Path

import duckdb


def analyse(source: Path, output: Path, minimum_flights: int = 100) -> dict:
    """Preserve raw values; exclude missing delay counts from rate estimates."""
    if minimum_flights < 1:
        raise ValueError("minimum_flights must be positive")
    with duckdb.connect() as con:
        con.execute(
            "CREATE TABLE raw_text AS SELECT * FROM read_csv(?, header=true, all_varchar=true)",
            [str(source)],
        )
        required = {
            "year",
            "month",
            "carrier",
            "airport",
            "arr_flights",
            "arr_del15",
            "arr_delay",
            "carrier_ct",
            "weather_ct",
            "nas_ct",
            "security_ct",
            "late_aircraft_ct",
            "carrier_delay",
            "weather_delay",
            "nas_delay",
            "security_delay",
            "late_aircraft_delay",
            "arr_cancelled",
            "arr_diverted",
        }
        columns = {row[0] for row in con.execute("DESCRIBE raw_text").fetchall()}
        if not required <= columns:
            raise ValueError(f"Missing columns: {sorted(required - columns)}")
        casts = ", ".join(
            f"CAST({name} AS DOUBLE) AS {name}"
            for name in sorted(required - {"carrier", "airport"})
        )
        try:
            con.execute(f"CREATE TABLE raw AS SELECT * REPLACE ({casts}) FROM raw_text")
        except duckdb.ConversionException as error:
            raise ValueError("Malformed numeric input") from error
        if con.execute("SELECT COUNT(*) FROM raw").fetchall()[0][0] == 0:
            raise ValueError("Empty input")
        count_columns = ["arr_flights", "arr_del15", "arr_cancelled", "arr_diverted"]
        cause_columns = sorted(
            required - {"year", "month", "carrier", "airport"} - set(count_columns)
        )
        invalid_numeric = " OR ".join(
            f"({name} IS NOT NULL AND (NOT isfinite({name}) OR {name} < 0))"
            for name in count_columns + cause_columns + ["year", "month"]
        )
        invalid_counts = " OR ".join(
            f"({name} IS NOT NULL AND {name} != floor({name}))"
            for name in count_columns
        )
        if con.execute(
            f"SELECT COUNT(*) FROM raw WHERE {invalid_numeric} OR {invalid_counts}"
        ).fetchall()[0][0]:
            raise ValueError("Invalid negative, non-finite or fractional count values")
        missing_by_column = {
            name: con.execute(
                f"SELECT COUNT(*) FROM raw WHERE {name} IS NULL"
            ).fetchall()[0][0]
            for name in sorted(required)
        }
        periods = con.execute(
            "SELECT DISTINCT year, month FROM raw ORDER BY year, month"
        ).fetchall()
        duplicates = con.execute("""
            SELECT COUNT(*) FROM (
                SELECT year, month, carrier, airport FROM raw
                GROUP BY ALL HAVING COUNT(*) > 1)
        """).fetchall()[0][0]
        invalid = con.execute("""
            SELECT COUNT(*) FROM raw WHERE year IS NULL OR month IS NULL
            OR month NOT BETWEEN 1 AND 12 OR carrier IS NULL OR airport IS NULL
            OR arr_flights IS NULL OR arr_flights < 0 OR arr_del15 < 0
            OR arr_del15 > arr_flights OR arr_delay < 0
            OR arr_cancelled < 0 OR arr_diverted < 0
            OR trim(carrier) = '' OR trim(airport) = ''
            OR year != floor(year) OR year < 1987 OR month != floor(month)
            OR arr_cancelled > arr_flights OR arr_diverted > arr_flights
            OR arr_del15 + arr_cancelled + arr_diverted > arr_flights
        """).fetchall()[0][0]
        if duplicates or invalid:
            raise ValueError(
                f"Unsafe input: duplicate keys={duplicates}, invalid rows={invalid}"
            )
        quality = con.execute("""
            SELECT COUNT(*), SUM(arr_flights), COUNT(*) FILTER (WHERE arr_del15 IS NULL),
                COUNT(*) FILTER (WHERE ABS(arr_delay - (carrier_delay + weather_delay
                    + nas_delay + security_delay + late_aircraft_delay)) > 1),
                COUNT(*) FILTER (WHERE ABS(arr_del15 - (carrier_ct + weather_ct
                    + nas_ct + security_ct + late_aircraft_ct)) > 0.05)
            FROM raw
        """).fetchall()[0]
        summary = con.execute("""
            SELECT SUM(arr_flights), SUM(arr_del15), SUM(arr_del15)/NULLIF(SUM(arr_flights),0)
            FROM raw WHERE arr_del15 IS NOT NULL
        """).fetchall()[0]
        con.execute("""
            CREATE VIEW segments AS
            SELECT carrier, airport, SUM(arr_flights) flights,
                SUM(arr_flights) FILTER (WHERE arr_del15 IS NOT NULL) rate_flights,
                SUM(arr_del15) delayed,
                SUM(arr_del15)/NULLIF(SUM(arr_flights) FILTER (WHERE arr_del15 IS NOT NULL),0) delay_rate,
                SUM(arr_delay) delay_minutes
            FROM raw GROUP BY carrier, airport
        """)
        rankings = {}
        for metric in ("delay_minutes", "delay_rate", "flights"):
            ranking_rows = con.execute(
                f"SELECT * FROM segments WHERE flights >= ? ORDER BY {metric} DESC NULLS LAST, carrier, airport LIMIT 10",
                [minimum_flights],
            ).fetchall()
            rankings[metric] = [
                dict(
                    zip(
                        (
                            "carrier",
                            "airport",
                            "flights",
                            "rate_flights",
                            "delayed",
                            "delay_rate",
                            "delay_minutes",
                        ),
                        row,
                        strict=True,
                    )
                )
                for row in ranking_rows
            ]
        missing_cause_rows = con.execute("""
            SELECT COUNT(*) FROM raw WHERE carrier_ct IS NULL OR weather_ct IS NULL
            OR nas_ct IS NULL OR security_ct IS NULL OR late_aircraft_ct IS NULL
            OR carrier_delay IS NULL OR weather_delay IS NULL OR nas_delay IS NULL
            OR security_delay IS NULL OR late_aircraft_delay IS NULL
        """).fetchall()[0][0]
        flagged_rows = con.execute("""
            SELECT year, month, carrier, airport FROM raw
            WHERE ABS(arr_delay - (carrier_delay + weather_delay + nas_delay + security_delay + late_aircraft_delay)) > 1
            OR ABS(arr_del15 - (carrier_ct + weather_ct + nas_ct + security_ct + late_aircraft_ct)) > 0.05
            ORDER BY year, month, carrier, airport
        """).fetchall()
        segments = con.execute(
            """
            SELECT carrier, airport, flights, delayed, delay_rate, delay_minutes
            FROM segments WHERE flights >= ? AND delay_rate IS NOT NULL
            ORDER BY delay_minutes DESC NULLS LAST, carrier, airport LIMIT 10
        """,
            [minimum_flights],
        ).fetchall()
    result = {
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "source_file": source.name,
        "periods": [dict(zip(("year", "month"), row, strict=True)) for row in periods],
        "missing_by_column": missing_by_column,
        "incomplete_cause_rows": missing_cause_rows,
        "reconciliation_flag_keys": [
            dict(zip(("year", "month", "carrier", "airport"), row, strict=True))
            for row in flagged_rows
        ],
        "rankings": rankings,
        "raw_rows": quality[0],
        "raw_reported_flights": quality[1],
        "missing_delay_count_rows": quality[2],
        "cause_minutes_mismatch_rows": quality[3],
        "cause_counts_mismatch_rows": quality[4],
        "rate_denominator_flights": summary[0],
        "delayed_flights": summary[1],
        "weighted_delay_rate": summary[2],
        "minimum_segment_flights": minimum_flights,
        "top_segments_by_reported_delay_minutes": [
            dict(
                zip(
                    (
                        "carrier",
                        "airport",
                        "flights",
                        "delayed",
                        "delay_rate",
                        "delay_minutes",
                    ),
                    row,
                    strict=True,
                )
            )
            for row in segments
        ],
    }
    output.mkdir(parents=True, exist_ok=True)
    (output / "audit.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    rate = summary[2]
    lines = [
        "# Aviation disruption diagnostic",
        "",
        f"Input: {quality[0]:,} monthly carrier-airport records; {quality[1]:,.0f} reported flights.",
        f"Missing delay count: {quality[2]} row(s), excluded from both rate numerator and denominator.",
        f"Cause reconciliation flags: {quality[3]} minute-total rows; {quality[4]} count-total rows.",
        f"Weighted 15+ minute arrival delay rate: {rate:.2%}."
        if rate is not None
        else "Delay rate undefined.",
        "",
        "## Investigation priorities",
        "",
        "Rank by total reported delay minutes to identify high-burden segments for investigation.",
        "Read alongside delay rate and traffic volume; this is not a ranking of airline quality.",
        "",
        "| Carrier | Airport | Reported flights | Delayed | Delay rate | Delay minutes |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for carrier, airport, flights, delayed, segment_rate, minutes in segments:
        burden = f"{minutes:.0f}" if minutes is not None else "unknown"
        lines.append(
            f"| {carrier} | {airport} | {flights:.0f} | {delayed:.0f} | {segment_rate:.1%} | {burden} |"
        )
    lines += [
        "",
        "## How the priority changes with the metric",
        "",
        "Delay rate measures frequency; total minutes measures burden; traffic measures exposure. These rankings answer different questions. Total minutes includes available raw burden even when delay counts are missing; rates exclude those records from numerator and denominator. Missing burden is unknown, never filled with zero.",
        "",
        "| Metric | Leading eligible segment | Value |",
        "|---|---|---:|",
        *[
            f"| {metric} | {entries[0]['carrier']}–{entries[0]['airport']} | {entries[0][metric]:.4f} |"
            for metric, entries in rankings.items()
            if entries and entries[0][metric] is not None
        ],
        "",
        "## Recommendation and feasibility limits",
        "",
        "Request flight-level schedules, turnaround/rotation histories and decision-time weather inputs for the highest-burden segments. Validate cause discrepancies with the provider before using cause shares to recommend interventions.",
        "",
        "Monthly aggregates support descriptive prioritisation, not pre-departure forecasting or causal claims. No fuel savings, airline deployment, predictive accuracy or operational benefit has been demonstrated. The minimum-volume threshold is a screening choice, not a statistical confidence guarantee.",
    ]
    (output / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, default=Path("reports"))
    parser.add_argument("--minimum-flights", type=int, default=100)
    arguments = parser.parse_args()
    print(
        json.dumps(
            analyse(arguments.source, arguments.output, arguments.minimum_flights),
            indent=2,
        )
    )
