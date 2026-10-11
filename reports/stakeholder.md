# Aviation investigation findings

Start with Delta–Atlanta and American–Dallas/Fort Worth for investigation of total arrival-delay burden. Request flight-level evidence before selecting an intervention. This independent AI-assisted prototype is not a customer study or NABLA product.

July 2026: 1,806 carrier-arrival-airport records, 697,754 reported flights and 189,830 known delayed arrivals. Excluding one missing count and its matching flight yields a 27.21% weighted delay rate. Nineteen distinct records fail both cause-count and cause-minute tolerances; provider clarification is needed rather than assuming source error.

| Segment | Flights | Delay rate | Delay minutes |
|---|---:|---:|---:|
| Delta–Atlanta (DL–ATL) | 21,771 | 23.5% | 450,182 |
| American–Dallas/Fort Worth (AA–DFW) | 14,742 | 27.0% | 423,138 |
| PSA–Washington Reagan (OH–DCA) | 3,553 | 34.8% | 172,041 |

DL–ATL leads burden and traffic. Among segments with at least 100 flights, QX–SFO leads rate at 75.84%. A high percentage in a smaller segment should not automatically outrank a larger burden without an agreed objective. Monthly aggregates cannot establish causes or intervention benefits.

The separate NYC 2013 departure experiment excludes 8,255 unknown outcomes from 336,776 records. The 54,145-flight test contains 3,718 severe delays. The median baseline beats the forest on MAE (16.25 versus 20.64 minutes). At 20 daily reviews, the forest finds 239 severe delays but generates 981 false alerts and misses 3,479 (6.4% recall). Nominal 90% intervals cover 85.4% overall and 80.6% in December. Constant-width intervals add no ranking benefit. These results do not support live adoption.

## Next requests

1. Confirm the customer's decision: repeated-delay investigation, protecting connections, reviewer workload or a specific airport objective.
2. Clarify cause discrepancies and compare several months before treating July as representative.
3. Obtain versioned day-ahead schedules, outcome-completeness flags, flight timings, rotations/turnarounds, crew/curfew constraints and archived decision-time weather forecasts with usage rights.
4. Agree reviewer capacity and false-alert/missed-event costs; the current 20-flight budget is provisional.
5. Predeclare alert-focused evaluation and rolling chronological holdouts using current data before adding complex models or adaptive uncertainty.

BizDev can scope data access and problem discovery; the Science Team can use the same definitions and exclusions for feasibility work. Different geography, periods, targets and grains prevent transferring this research to the monthly sample or Japanese operations. No airline production requirements, causal savings or NABLA service effects have been validated.
