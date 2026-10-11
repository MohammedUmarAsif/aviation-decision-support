# Methodology and limitations

Diagnostic user: hypothetical airline operations analyst. Decision: select carrier-arrival-airport segments for investigation using monthly retrospective data. Rank total minutes to locate burden, then compare frequency and traffic. The 100-flight minimum is a screen, not a confidence guarantee. No customer interview or intervention effect has been measured.

Predictive user: hypothetical operations planning reviewer. Decision: choose up to 20 next-day flights for manual review at day-ahead planning. Target: signed departure delay in minutes; severe event: at least 60 minutes. Lead time varies by scheduled hour. Feature availability is assumed from schedule proxies. The capacity and severe-event threshold are AI-proposed demonstration choices awaiting personal/customer review.

## Chronological experiment

| 2013 partition | Dates | Purpose |
|---|---|---|
| Train | January–June | Fit preprocessing and models |
| Validation | July–August | Select using MAE |
| Calibration | September–October | Estimate interval radius |
| Test | November–December | Report frozen-model performance |

No random split, future outcomes in features, test tuning or model refit. Encoding fits training categories only and handles unseen categories. The baseline predicts the training median (-1 minute). One bounded random forest uses 40 trees, depth 12, minimum leaf size 100, seed 42. Settings were chosen for a small computational demonstration before viewing results, without a hyperparameter search.

MAE is mean absolute error in minutes. Medians minimize absolute error. The forest uses default squared-error training, so its mean-oriented predictions can rank risky schedules while losing on MAE. This mismatch is disclosed rather than optimized away after test inspection. The median wins validation, freezing model selection before calibration/test. Both test queues show trade-offs; a future alert-focused study needs a predeclared selection criterion and fresh test data.

## Review capacity and uncertainty

Rank predictions within each day and take up to 20 eligible flights. Ties use schedule keys deterministically. The constant baseline is therefore an arbitrary reproducible control queue, not random or an established operational baseline. Precision = severe outcomes among alerts / alerts; recall = severe outcomes among alerts / all eligible severe outcomes. False alerts consume reviews without finding severe delay; missed disruptions are severe outcomes outside the queue. These metrics are conditional on known outcomes and exclude cancellation performance.

Split conformal uses absolute calibration residuals: the ceil((n+1) × 0.9)-th order statistic determines the radius. Intervals are prediction ± radius; negative endpoints are retained because early departures are valid. Calibration samples too small for a finite radius are rejected. Report empirical coverage overall/by month and interval width. Temporal dependence and changing distributions undermine the usual exchangeability assumption; nominal 90% is not a guarantee for each flight.

Lower interval endpoints are also ranked at the same budget. Subtracting a constant radius preserves rankings, so no additional alert usefulness is demonstrated by these intervals. Adaptive conformal methods from the Japanese study are not implemented. Probability calibration, conditional coverage, rolling-origin tests and capacity/cost sensitivity remain planned. No probability-calibration claim is made.

## Next evidence and limits

Obtain versioned day-ahead schedules and outcome completeness, then decision timestamps, rotation/turnaround links, crew/curfew constraints and archived weather forecasts. Realized weather must not substitute for forecasts available at the decision. External data should be joined as-of that timestamp.

NYC 2013 does not establish relevance to current Japanese operations. Monthly arrival diagnosis and flight departure research differ in target, period, geography and grain; do not combine them into a single validation claim. Seasonal change is compatible with December undercoverage, but this experiment does not identify its cause. Prospective domain review is needed. No aircraft swaps, safety decisions, fuel savings, service effects, profitability or production reliability have been demonstrated.
