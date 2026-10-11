# Data dictionary and provenance

## Monthly diagnostic

Source: [BTS delay causes](https://transtats.bts.gov/OT_Delay/ot_delaycause1.asp). The official page displayed July 2026 when checked on 11 October 2026. It defines delay as arrival at least 15 minutes after schedule and prorates cause counts across causes.

The local download existed before this session. Its reported retrieval date is 11 October 2026; the acquisition event was not independently witnessed here. The analyzed CSV has SHA256 `ef188f572d9fdaf89a095acea2f78dd459e92894fa683112b94425e869c618e3`, and local year/month values confirm July 2026. This verifies analyzed bytes and period, not the full acquisition chain.

Use the official page's **Download Raw Data** link, select July 2026 and extract `Airline_Delay_Cause.csv` into `data/raw/`. Compare hashes before expecting identical results. Provider revisions can change results. The previous README recorded this URL:

`https://transtats.bts.gov/OT_Delay/ot_delaycause1_DL.aspx?8n4=9ur4r+Brn4z106u+or69rr0+FHGEM+NaQ+FHGEM`

Opaque parameters are not a stable API. The audit records periods and hashes on every run. BTS makes these statistics public, but a dataset-specific redistribution license was not established here. Raw BTS files and the Excel dictionary are withheld; only derived findings and download instructions are published.

Grain: one `(year, month, carrier, airport)` record, where airport is the arrival airport. This is not a route or individual flight. Interpret carrier codes using provider reporting categories and codeshare notes.

| Field | Meaning and unit | Treatment |
|---|---|---|
| year, month | Reporting year/month | Required whole numbers; month 1–12 |
| carrier, airport | Reporting carrier and arrival-airport codes | Required nonblank keys |
| arr_flights | Reported flights | Required, finite, nonnegative whole count |
| arr_del15 | Arrivals delayed 15+ minutes | Missing allowed; excluded with matching flights from rate; cannot exceed flights |
| arr_delay | Total delayed-arrival minutes | Missing remains unknown; available burden summed separately from rate eligibility |
| carrier_ct, weather_ct, nas_ct, security_ct, late_aircraft_ct | Prorated count by cause | Fractional counts allowed; finite nonnegative or flagged missing |
| carrier_delay, weather_delay, nas_delay, security_delay, late_aircraft_delay | Minutes by cause | Finite nonnegative or flagged missing |
| arr_cancelled, arr_diverted | Cancelled/diverted counts | Missing recorded; known values whole, finite and between zero and flights |

Rate = sum of known delayed counts / sum of flights on those same records. This is not a mean of percentages or a completed-flight denominator. Reconciliation tolerances are 0.05 prorated flights and 1 minute: provisional screening choices, not provider-approved error bounds. Missing causes make reconciliation unavailable. Duplicate keys and invalid values fail before new reports are written. Raw bytes remain unchanged.

## Flight research

[nycflights13](https://github.com/tidyverse/nycflights13) provides NYC outbound 2013 flight records originally sourced from BTS. Its pinned [DESCRIPTION](https://github.com/tidyverse/nycflights13/blob/df98ef215aa8216fe0838a0b8ac5bada646d814c/DESCRIPTION) specifies CC0. Raw files remain excluded to keep the repository small. `reports/flights.provenance.json` records source URL, commit, retrieval timestamp, RDA/CSV hashes and row count. Conversion uses pyreadr/pandas versions from `uv.lock`.

Grain: one flight. Proposed key: year/month/day/carrier/flight/origin/scheduled departure time; checked for nulls and duplicates before exclusions.

| Field | Role | Availability assumption |
|---|---|---|
| year, month, day | Dates and splits | Scheduled date; 2013 required |
| carrier, origin, dest | Model categories | Assumed known in day-ahead schedule |
| hour | Scheduled local departure hour | Not actual departure hour |
| weekday | Date-derived feature | Known at planning time |
| distance | Route distance, miles | Schedule proxy; real snapshots needed |
| flight, sched_dep_time | Keys and tie-breaking | Schedule identifiers, not target features |
| dep_delay | Target, signed minutes | Outcome only; early departures remain negative |

8,255 unknown departure-delay outcomes are excluded; they cannot automatically be labeled cancellations. Actual times, arrival delays, tail number, air time, causes and observed weather are excluded from model features. The archive has no authenticated day-ahead snapshots: feature availability is an assumption, not demonstrated operational availability. Unknown outcomes prevent cancellation evaluation and can bias the queue.
