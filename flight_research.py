"""Schedule-only retrospective departure-delay experiment, with temporal holdouts."""

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder

FEATURES = ["carrier", "origin", "dest", "hour", "weekday", "distance"]
KEY = ["year", "month", "day", "carrier", "flight", "origin", "sched_dep_time"]


def prepare(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Fail on unsafe keys; retain early departures, exclude unknown outcomes explicitly."""
    required = set(KEY + ["dep_delay", "dest", "hour", "distance"])
    if not required <= set(frame.columns):
        raise ValueError(f"Missing columns: {sorted(required - set(frame.columns))}")
    if frame[KEY].isna().any().any() or frame.duplicated(KEY).any():
        raise ValueError("Missing or duplicate flight keys")
    frame = frame.copy()
    frame["date"] = pd.to_datetime(frame[["year", "month", "day"]], errors="raise")
    if not (frame["year"] == 2013).all():
        raise ValueError("This experiment requires the documented 2013 dataset")
    numeric = frame[["dep_delay", "distance", "hour"]]
    if np.isinf(numeric.to_numpy(dtype=float)).any():
        raise ValueError("Non-finite values")
    if (frame["distance"] < 0).any() or (~frame["hour"].between(0, 23)).any():
        raise ValueError("Invalid schedule features")
    if frame[["carrier", "origin", "dest", "distance", "hour"]].isna().any().any():
        raise ValueError("Missing schedule features")
    quality = {
        "raw_flights": len(frame),
        "missing_departure_delay": int(frame.dep_delay.isna().sum()),
    }
    frame = frame.loc[frame.dep_delay.notna()].copy()
    frame["weekday"] = frame.date.dt.dayofweek
    return frame.sort_values(KEY).reset_index(drop=True), quality


def temporal_split(frame: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """No random split: fit Jan-Jun, select Jul-Aug, calibrate Sep-Oct, test Nov-Dec."""
    parts = {
        "train": frame.loc[frame.month <= 6],
        "validation": frame.loc[frame.month.between(7, 8)],
        "calibration": frame.loc[frame.month.between(9, 10)],
        "test": frame.loc[frame.month >= 11],
    }
    if any(part.empty for part in parts.values()):
        raise ValueError("All four chronological partitions must be nonempty")
    return parts


def conformal_radius(residuals: np.ndarray, alpha: float = 0.1) -> float:
    """Finite sample order statistic; no temporal exchangeability guarantee claimed."""
    if not 0 < alpha < 1 or len(residuals) == 0 or not np.isfinite(residuals).all():
        raise ValueError("Invalid conformal inputs")
    rank = math.ceil((len(residuals) + 1) * (1 - alpha))
    if rank > len(residuals):
        raise ValueError("Insufficient calibration examples for finite radius")
    return float(np.sort(residuals)[rank - 1])


def alert_metrics(frame: pd.DataFrame, scores: np.ndarray, capacity: int = 20) -> dict:
    """Rank each day's eligible flights using a deterministic schedule key for ties."""
    if capacity < 1 or len(scores) != len(frame) or not np.isfinite(scores).all():
        raise ValueError("Invalid alert inputs")
    ranked = frame.assign(score=scores).sort_values(
        ["date", "score"] + KEY, ascending=[True, False] + [True] * len(KEY)
    )
    selected = ranked.groupby("date", sort=False).head(capacity)
    disruptions = int((frame.dep_delay >= 60).sum())
    hits = int((selected.dep_delay >= 60).sum())
    return {
        "capacity_per_day": capacity,
        "alerts": len(selected),
        "hits": hits,
        "false_alerts": len(selected) - hits,
        "missed_disruptions": disruptions - hits,
        "precision": hits / len(selected) if len(selected) else None,
        "recall": hits / disruptions if disruptions else None,
    }


def evaluate(source: Path, output: Path, capacity: int = 20) -> dict:
    frame, quality = prepare(pd.read_csv(source))
    parts = temporal_split(frame)
    train = parts["train"]
    median = float(train.dep_delay.median())
    preprocessor = ColumnTransformer(
        [
            (
                "category",
                OneHotEncoder(handle_unknown="ignore"),
                ["carrier", "origin", "dest"],
            ),
            ("number", "passthrough", ["hour", "weekday", "distance"]),
        ]
    )
    model = make_pipeline(
        preprocessor,
        RandomForestRegressor(
            n_estimators=40,
            max_depth=12,
            min_samples_leaf=100,
            random_state=42,
            n_jobs=2,
        ),
    )
    model.fit(train[FEATURES], train.dep_delay)
    predictions = {
        name: model.predict(part[FEATURES])
        for name, part in parts.items()
        if name != "train"
    }
    validation = parts["validation"]
    validation_mae = {
        "train_median": float(
            mean_absolute_error(validation.dep_delay, np.full(len(validation), median))
        ),
        "random_forest": float(
            mean_absolute_error(validation.dep_delay, predictions["validation"])
        ),
    }
    selected = min(validation_mae, key=lambda name: validation_mae[name])
    # Frozen selection before calibration/test. No hyperparameter search or test refit.
    calibration = parts["calibration"]
    test = parts["test"]
    chosen_cal = (
        predictions["calibration"]
        if selected == "random_forest"
        else np.full(len(calibration), median)
    )
    chosen_test = (
        predictions["test"]
        if selected == "random_forest"
        else np.full(len(test), median)
    )
    radius = conformal_radius(np.abs(calibration.dep_delay.to_numpy() - chosen_cal))
    covered = np.abs(test.dep_delay.to_numpy() - chosen_test) <= radius
    metrics: dict[str, dict[str, Any]] = {}
    capacities = {}
    for name, scores in {
        "train_median": np.full(len(test), median),
        "random_forest": predictions["test"],
    }.items():
        metrics[name] = {
            "mae_minutes": float(mean_absolute_error(test.dep_delay, scores)),
            "alerts": alert_metrics(test, scores, capacity),
        }
        capacities[name] = {
            str(budget): alert_metrics(test, scores, budget)
            for budget in (10, 20, 40, 80)
        }
    monthly = {
        str(month): {
            "flights": int((test.month == month).sum()),
            "coverage": float(covered[test.month == month].mean()),
        }
        for month in sorted(test.month.unique())
    }
    # Uncertainty-aware scores: lower interval endpoint. Constant radius preserves ordering.
    uncertainty_alerts = alert_metrics(test, chosen_test - radius, capacity)
    result = {
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "quality": quality,
        "features": FEATURES,
        "partitions": {
            name: {
                "flights": len(part),
                "start": str(part.date.min().date()),
                "end": str(part.date.max().date()),
            }
            for name, part in parts.items()
        },
        "train_median_minutes": median,
        "validation_mae_minutes": validation_mae,
        "selected_by_validation_mae": selected,
        "test": metrics,
        "split_conformal": {
            "nominal_coverage": 0.9,
            "radius_minutes": radius,
            "width_minutes": 2 * radius,
            "test_coverage": float(covered.mean()),
            "monthly": monthly,
            "lower_bound_alerts": uncertainty_alerts,
        },
        "limit": "Historical 2013 NYC schedule proxy; completed flights only; no operational or causal validation.",
    }
    output.mkdir(parents=True, exist_ok=True)
    (output / "capacities.json").write_text(
        json.dumps(
            {
                "study_id": "nyc-departure-2013-v1",
                "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                "test_days": int(test.date.nunique()),
                "severe_outcomes": int((test.dep_delay >= 60).sum()),
                "severe_threshold_minutes": 60,
                "models": capacities,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (output / "forecast.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Flight forecast research",
        "",
        "Retrospective 2013 NYC departure-delay experiment. See docs/methodology.md for availability assumptions and limitations.",
        "",
        f"Raw flights: {quality['raw_flights']:,}; unknown departure delays excluded: {quality['missing_departure_delay']:,}.",
        "",
        "| Model | Test MAE minutes | Alerts | Hits | False alerts | Missed 60+ minute delays | Precision | Recall |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for name, metric in metrics.items():
        a = metric["alerts"]
        lines.append(
            f"| {name} | {metric['mae_minutes']:.2f} | {a['alerts']} | {a['hits']} | {a['false_alerts']} | {a['missed_disruptions']} | {a['precision']:.1%} | {a['recall']:.1%} |"
        )
    lines += [
        "",
        f"Selected using July-August MAE: **{selected}**. Calibration is September-October; untouched test is November-December.",
        "",
        f"Nominal 90% split-conformal interval: radius {radius:.2f} minutes, width {2 * radius:.2f}; test coverage {covered.mean():.1%}.",
        "",
        "| Test month | Flights | Empirical coverage |",
        "|---|---:|---:|",
    ]
    for month, entry in monthly.items():
        lines.append(f"| {month} | {entry['flights']} | {entry['coverage']:.1%} |")
    lines += [
        "",
        "## Recommendation",
        "",
        "Evaluate MAE and alert usefulness separately. A mean-oriented model can rank disruptions yet lose to a median baseline on MAE. Do not adopt a model solely because it is more complex.",
        "",
        "The lower conformal endpoint provides a conservative score, but a constant interval radius cannot improve fixed-capacity rankings. No additional alert benefit is demonstrated by these intervals. Temporal dependence and drift invalidate an unconditional exchangeability-based coverage claim.",
        "",
        "The queue reviews at most 20 eligible flights daily by default using day-ahead schedule proxies. Unknown outcomes are absent from evaluation, so this cannot measure cancellation alerts or a live queue. Confirm schedule snapshots, reviewer capacity, rotation data and current local conditions before prospective testing. No cost savings or causal delay reductions have been demonstrated.",
    ]
    (output / "forecast.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, default=Path("reports"))
    parser.add_argument("--capacity", type=int, default=20)
    args = parser.parse_args()
    print(json.dumps(evaluate(args.source, args.output, args.capacity), indent=2))
