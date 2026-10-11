# Public claims register

The v1 page reads `site/evidence.json`, produced by `scripts/export_public.py` from checked derived reports. Agent execution checks do not imply independent peer review or completed owner comprehension.

| Claim | Evidence | Interpretation boundary |
|---|---|---|
| Delta–Atlanta leads eligible July 2026 delay minutes and traffic; QX–SFO leads rate | Full monthly aggregates; `reports/audit.json` rankings | Carrier plus arrival airport, not route or airline quality |
| 1,806 records, 697,754 reported flights, 697,753 matched rate denominator | Complete aggregate reconciliation; raw hash in audit | One unknown delay count; no imputed zero |
| Nineteen distinct records have cause reconciliation flags | Audit keys and per-segment flag counts | Provisional tolerances; no cause corrections or causal attribution |
| Median baseline has 16.25 test MAE versus forest 20.64 minutes | Frozen `reports/forecast.json`; reproducible within 1e-8 | Median won validation MAE; test queues do not reverse selection |
| At 20/day forest finds 239 severe delays; baseline 120 | `reports/capacities.json`; original alerts unchanged | 1,220 reviews each; 3,718 eligible severe outcomes; unknown outcomes excluded |
| Capacity controls show measured 10/20/40/80 queues | One run's frozen test scores, identical eligibility and tie rules | No interpolation, browser inference, new training or intervention benefit |
| Median interval coverage is 85.45%; December 80.55% | Split-conformal report, month-level coverage | 90% nominal target missed; intervals belong to median only; no flight probability guarantee |
| Page supports a discovery/feasibility discussion | Explicit decision, methods, limitations and evidence requests | No NABLA affiliation, internal product need, job eligibility or operational adoption |

Not claimed: causal delay reduction, fuel or financial savings, safety suitability, live prediction, current Japanese validity, adaptive conformal reproduction, cancellation performance, independent human authorship or personal approval of all methods.

BTS raw redistribution rights were not established. Publish only the reviewed derived aggregates. nycflights13's pinned metadata specifies CC0. Raw files, CVs, credentials and private documents remain excluded.

Future study: freeze v1; obtain bounded recent data and authenticated decision-time inputs, add historical severe-rate controls, predeclare alert-focused selection and cost/capacity criteria, evaluate multiple fresh chronological windows and improve unknown-outcome handling. Publication does not mean these future steps were completed.
