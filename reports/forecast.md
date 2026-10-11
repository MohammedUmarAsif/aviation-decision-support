# Flight forecast research

Retrospective 2013 NYC departure-delay experiment. See docs/methodology.md for availability assumptions and limitations.

Raw flights: 336,776; unknown departure delays excluded: 8,255.

| Model | Test MAE minutes | Alerts | Hits | False alerts | Missed 60+ minute delays | Precision | Recall |
|---|---:|---:|---:|---:|---:|---:|---:|
| train_median | 16.25 | 1220 | 120 | 1100 | 3598 | 9.8% | 3.2% |
| random_forest | 20.64 | 1220 | 239 | 981 | 3479 | 19.6% | 6.4% |

Selected using July-August MAE: **train_median**. Calibration is September-October; untouched test is November-December.

Nominal 90% split-conformal interval: radius 28.00 minutes, width 56.00; test coverage 85.4%.

| Test month | Flights | Empirical coverage |
|---|---:|---:|
| 11 | 27035 | 90.4% |
| 12 | 27110 | 80.6% |

## Recommendation

Evaluate MAE and alert usefulness separately. A mean-oriented model can rank disruptions yet lose to a median baseline on MAE. Do not adopt a model solely because it is more complex.

The lower conformal endpoint provides a conservative score, but a constant interval radius cannot improve fixed-capacity rankings. No additional alert benefit is demonstrated by these intervals. Temporal dependence and drift invalidate an unconditional exchangeability-based coverage claim.

The queue reviews at most 20 eligible flights daily by default using day-ahead schedule proxies. Unknown outcomes are absent from evaluation, so this cannot measure cancellation alerts or a live queue. Confirm schedule snapshots, reviewer capacity, rotation data and current local conditions before prospective testing. No cost savings or causal delay reductions have been demonstrated.
