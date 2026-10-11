# Aviation disruption diagnostic

Input: 1,806 monthly carrier-airport records; 697,754 reported flights.
Missing delay count: 1 row(s), excluded from both rate numerator and denominator.
Cause reconciliation flags: 19 minute-total rows; 19 count-total rows.
Weighted 15+ minute arrival delay rate: 27.21%.

## Investigation priorities

Rank by total reported delay minutes to identify high-burden segments for investigation.
Read alongside delay rate and traffic volume; this is not a ranking of airline quality.

| Carrier | Airport | Reported flights | Delayed | Delay rate | Delay minutes |
|---|---|---:|---:|---:|---:|
| DL | ATL | 21771 | 5119 | 23.5% | 450182 |
| AA | DFW | 14742 | 3973 | 27.0% | 423138 |
| UA | ORD | 9376 | 2431 | 25.9% | 248620 |
| AA | CLT | 9605 | 2397 | 25.0% | 230488 |
| OO | ORD | 8087 | 2077 | 25.7% | 221281 |
| AA | ORD | 5993 | 1683 | 28.1% | 195896 |
| UA | EWR | 5650 | 1587 | 28.1% | 183628 |
| UA | DEN | 9849 | 1985 | 20.2% | 179592 |
| OH | DCA | 3553 | 1237 | 34.8% | 172041 |
| AA | MIA | 5618 | 1646 | 29.3% | 164229 |

## How the priority changes with the metric

Delay rate measures frequency; total minutes measures burden; traffic measures exposure. These rankings answer different questions. Total minutes includes available raw burden even when delay counts are missing; rates exclude those records from numerator and denominator. Missing burden is unknown, never filled with zero.

| Metric | Leading eligible segment | Value |
|---|---|---:|
| delay_minutes | DL–ATL | 450182.0000 |
| delay_rate | QX–SFO | 0.7584 |
| flights | DL–ATL | 21771.0000 |

## Recommendation and feasibility limits

Request flight-level schedules, turnaround/rotation histories and decision-time weather inputs for the highest-burden segments. Validate cause discrepancies with the provider before using cause shares to recommend interventions.

Monthly aggregates support descriptive prioritisation, not pre-departure forecasting or causal claims. No fuel savings, airline deployment, predictive accuracy or operational benefit has been demonstrated. The minimum-volume threshold is a screening choice, not a statistical confidence guarantee.
