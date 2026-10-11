# Learning milestones

Work one row at a time. Record completion only after an actual response or demonstrated check.

| Milestone | Concept | Small exercise and explanation | State |
|---|---|---|---|
| Monthly diagnosis | Rates versus volumes | Compare 20/100 with 100/1,000; explain why a lower rate can mean more delayed flights | User answered correctly |
| Data quality | Missing is unknown | Read `test_missing_is_not_zero`; explain its rate denominator | Pending |
| Python functions | Inputs and returned results | Find `analyse(source, output)`; identify the file input and returned rate | Pending |
| Forecast evaluation | MAE averages error sizes | Predictions [0,10], actual [10,30] give errors [10,20] and MAE 15; explain why compare a baseline | Pending |
| Temporal splits | Future outcomes unavailable | Locate four periods in `temporal_split`; explain why November is absent from training | Pending |
| Alerts | Reviews have workload costs | 239 hits in 1,220 reviews means 981 false alerts; explain what a reviewer needs before adoption | Pending |
| Uncertainty | Targets differ from measured coverage | Compare 90% nominal with December's 80.6%; explain why no 90%-reliable-flight claim | Pending |
| Publication | Same inputs and environment | Run demo and pytest; explain what synthetic data can demonstrate | Pending |

Carrier means airline reporting code; airport is the arrival airport in the monthly audit. Delay rate is the percentage arriving 15+ minutes late. Burden adds delay minutes. Traffic counts flights. A baseline is a simple comparator; a holdout is kept separate from fitting. An interval describes a possible-outcome range, not an operational certification.

The completed arithmetic exercise demonstrates that specific distinction, not implementation review or forecasting-method mastery.
