# Validation evidence

Checked 11 October 2026. These are AI-agent execution checks, not independent peer review or personal mastery.

| Check | Observed result |
|---|---|
| Original pipeline and tests before changes | Seven original tests passed with documented `python -m pytest`; milestone totals reproduced |
| Expanded pytest suite | 21 cases covering matched denominators, missing counts/causes/burden, empty inputs, duplicates, negative/nonfinite/fractional counts, temporal partitions, conformal order statistic and review queues |
| Ruff lint and format | Passed |
| ty type check | Passed; not a proof of dataframe schemas or analytical correctness |
| Offline synthetic demo | Passed; explicit synthetic inputs, no observed-airline claim |
| Monthly raw-file audit | 1,806 rows; 697,754 flights; 697,753 rate denominator; 189,830 delayed; 27.2059% rate |
| Reconciliation | 19 minute flags and 19 count flags on the same 19 distinct keys; raw values retained |
| Flight-level research | 336,776 raw; 8,255 unknown outcomes excluded; chronological train 161,275 / validation 57,326 / calibration 55,775 / test 54,145 |
| Forecast evidence | Median wins validation MAE; test MAE 16.2543 vs forest 20.6408 minutes |
| Interval evaluation | 56-minute width; 85.4465% test coverage; November 90.3532%, December 80.5533% |
| Local Docker | Daemon unavailable; Docker build and synthetic container run both passed in GitHub CI |
| GitHub publication and CI | Public repository verified; quality and research jobs passed on commit `46f9f12c4eda0a28e57d98dbf295b2d2d8dfbf80` in [run 38140236266](https://github.com/MohammedUmarAsif/aviation-decision-support/actions/runs/38140236266) |

The new audit also preserves available burden when delayed-flight counts are unknown. This intentionally separates burden eligibility from rate eligibility; the existing July top-ten results remain unchanged. A newly failed run does not overwrite previous reports, so existing outputs should not be mistaken for evidence of success on failed input.

The recorded flight report is frozen. CI re-downloaded the pinned public data, reran the full experiment on Linux, and successfully compared JSON results at 1e-8 tolerance against the Windows-generated record. Source-file hashes, periods and excluded counts are recorded. The inherited BTS acquisition history is only partly verified; a provider re-download may be revised. Raw redistribution rights were not established for BTS, so raw files remain excluded.

Limitations: no contemporary Japanese data, authenticated schedule snapshots, flight cancellations model, decision-time weather/rotation features, prospective customer evaluation, probability calibration, adaptive conformal method, causal intervention study or operational deployment. User review is narrow and documented separately.

## Interactive release — 12 October 2026

The original metrics reproduced unchanged; complete monthly segment exports and measured 10/20/40/80 capacity grids reconcile to frozen reports. Expanded suite: 27 cases, with Ruff, format, ty and JavaScript syntax passing. Linux CI reproduced both the forecast and capacity-grid JSON within 1e-8. The interactive page was published through Actions Pages and verified by HTTP, deployed evidence hashes, actual desktop/mobile rendering, shared-state reload and brief download. See [UI validation](UI_VALIDATION.md) for exact release links, screenshots and check boundaries.
