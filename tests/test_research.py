import numpy as np
import pandas as pd
import pytest

from flight_research import (
    FEATURES,
    alert_metrics,
    conformal_radius,
    prepare,
    temporal_split,
)


def flights():
    return pd.DataFrame(
        [
            dict(
                year=2013,
                month=m,
                day=1,
                carrier="AA",
                flight=i,
                origin="JFK",
                dest="LAX",
                sched_dep_time=800,
                hour=8,
                distance=2400,
                dep_delay=d,
            )
            for i, (m, d) in enumerate(
                zip([1, 7, 9, 11, 11], [-5, 10, 20, 70, None], strict=True)
            )
        ]
    )


def test_split_and_unknown_outcomes():
    frame, quality = prepare(flights())
    parts = temporal_split(frame)
    assert quality == {"raw_flights": 5, "missing_departure_delay": 1}
    assert parts["train"].dep_delay.iloc[0] == -5
    ordered = list(parts.values())
    assert all(
        a.date.max() < b.date.min() for a, b in zip(ordered, ordered[1:], strict=False)
    )
    assert not set(FEATURES) & {
        "dep_delay",
        "arr_delay",
        "dep_time",
        "arr_time",
        "tailnum",
        "air_time",
    }


def test_duplicate_key_rejected():
    frame = flights().iloc[:1]
    with pytest.raises(ValueError, match="duplicate"):
        prepare(pd.concat([frame, frame]))


def test_conformal_order_statistic():
    assert conformal_radius(np.arange(1, 10)) == 9
    with pytest.raises(ValueError):
        conformal_radius(np.array([]))
    with pytest.raises(ValueError):
        conformal_radius(np.array([1.0]))


def test_capacity_and_false_alerts():
    frame, _ = prepare(flights().iloc[:4])
    frame["date"] = pd.Timestamp("2013-11-01")
    result = alert_metrics(frame, np.array([4, 3, 2, 1]), capacity=2)
    assert result["alerts"] == 2
    assert result["hits"] == 0
    assert result["false_alerts"] == 2
    assert result["missed_disruptions"] == 1
    assert alert_metrics(frame, np.array([4, 3, 2, 1]) - 50, 2) == result


def test_tied_scores_are_stable():
    frame, _ = prepare(flights().iloc[:4])
    frame["date"] = pd.Timestamp("2013-11-01")
    forward = alert_metrics(frame, np.ones(4), 1)
    backward = alert_metrics(frame.iloc[::-1], np.ones(4), 1)
    assert forward == backward
