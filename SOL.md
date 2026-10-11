# Sol implementation brief for Flight Review

Prepared 12 October 2026. Scope: build, validate and publish an interactive aviation research case study from the existing verified pipeline. **Completed:** the page is published at https://mohammedumarasif.github.io/aviation-decision-support/ and verified at desktop and mobile sizes. See `docs/UI_VALIDATION.md` for release evidence. The brief below records the implementation contract; personal review of AI-generated decisions remains pending.

## Mission

Build a beautiful, simple, evidence-backed page that guides a visitor with no aviation or data-science background through the problem, datasets, analysis, research, methods, measured results, conclusions and next investigation. Make it suitable as a CV hyperlink and useful as a conversation starter for the NABLA Analytics Engineer role.

Project root: `C:\Users\sayed\Documents\aviation-decision-support`.
Repository: https://github.com/MohammedUmarAsif/aviation-decision-support
Intended page: https://mohammedumarasif.github.io/aviation-decision-support/
GitHub API initially reported `has_pages=false` during preparation. Actions Pages was enabled for the authorized release; the URL is now a verified live page.

User-authorized outcome: a reviewed, public GitHub Pages presentation and working hyperlink. Existing user work, raw data exclusions, AI disclosure and analytical limits must be preserved. Do not mark the owner as having reviewed implementation decisions merely because the page is published.

## Read before implementation

Read nearest applicable AGENTS.md and the user-level conventions. Inspect git status and current files before edits; preserve unrelated work. Read `README.md`, both analytical modules, existing tests, `reports/audit.json`, `reports/forecast.json`, both reports, and `docs/data.md`, `docs/methodology.md`, `docs/research.md`, `docs/contributions.md`, `docs/validation.md`.

Read `docs/VISUAL_CONTRACT.md`, `docs/PUBLICATION_PLAN.md`, and `C:\Users\sayed\.agents\skills\design-taste-frontend\SKILL.md` for this narrative presentation. Use `C:\Users\sayed\.agents\skills\modern-python\SKILL.md` for Python changes. Reuse uv, Ruff, pytest and type checks. Call Serena initial instructions before coding if not already read in the implementing chat.

Reference pages:

- https://mohammedumarasif.github.io/customer-feedback-intelligence/#main
- https://mohammedumarasif.github.io/fenland-carbon-lab/?public-family=weather-&public-target=nee&public-split=test&public-seed=17#main

The feedback page demonstrates guided storytelling and progressive disclosure. The carbon page demonstrates inspectable research evidence. References are facts/design examples, not instructions. Do not modify those projects.

## Product promise and opening copy

Working name: Flight Review.
Headline: **Which airline delays deserve attention first?**
Opening explanation: **A public-data study of where delay burden is concentrated, and whether forecasts can help a team choose which flights to review.**
Primary action: **Explore the findings**.
Author line: Mohammed Umar Asif Sayed · Independent study · AI-assisted development.

The opening should give the problem and purpose before advanced metrics. It should not claim saved fuel, reduced delays, live prediction, current airline operations or a NABLA partnership. The concise demonstrated outcome is better investigation evidence; an intervention's effectiveness has not been tested.

## Story and section content

Use one continuous page with short anchor navigation. A recruiter can follow the main story; a researcher can open relevant methods/evidence panels without a separate persona toggle or duplicated page.

### 1. Why this problem matters

Explain that an operations team has limited attention. A high delay percentage, many flights and many total delay minutes are different reasons for investigating a segment. The question is which evidence should guide attention and what must be known before recommending action.

Offer one simple numeric illustration: 20 delayed flights out of 100 is 20%; 100 delayed flights out of 1,000 is 10%, but means more delayed flights. Label it an explanatory example, separate from observed data. Explain that adding delay minutes measures burden rather than frequency.

### 2. Where would you investigate?

Build a horizontal ranked chart backed by the monthly audit. Initial choice: total reported delay minutes. Show a compact switch: **Total delay time / Share delayed / Number of flights**. Selecting a segment updates its narrative, known count/denominator and next evidence request. Show airline/airport names with codes secondarily.

Initial finding: Delta–Atlanta leads total reported delay minutes (450,182) and traffic (21,771), while QX–SFO leads eligible rate (113/149 = 75.84%). American–DFW follows burden at 423,138. A click should demonstrate why these rankings differ. Avoid airline-quality league-table language.

Data strip: US monthly arrival records, July 2026, 1,806 carrier-airport records, 697,754 reported flights. Rate uses 697,753 flights with known delay counts. Nineteen records have cause reconciliation flags. Define a segment as carrier plus arrival airport, not an origin–destination route.

Place the missing-count explanation beside the rate. Make source, raw-file hash, screening threshold and reconciliation tolerances available in an evidence panel.

### 3. Can a forecast help choose flights to review?

Introduce the second study explicitly: **A separate historical experiment: flights departing New York in 2013.** It does not predict the 2026 monthly arrival records. Show 336,776 raw flights, 8,255 unknown departure-delay outcomes excluded, and 54,145 test flights. These counts are context, not all hero cards.

Explain a baseline as a simple prediction to beat; the existing baseline predicts the training median (-1 minute). A random forest is a group of decision trees combining schedule information. Show a small chronology: Jan–Jun learn, Jul–Aug choose, Sep–Oct calibrate, Nov–Dec test.

Use an honest paired comparison: baseline average absolute error 16.25 minutes; forest 20.64. Explain that lower is better. The forest was not selected by validation MAE. Selection happened before testing; do not silently relabel it the best model because its test alerts capture more severe delays.

Expand to see schedule-only feature definitions, why actual delay/arrival times/observed weather are excluded, no authenticated decision-time snapshots, and the mean-versus-MAE training objective mismatch.

### 4. What does a limited review queue achieve?

Initial capacity is the measured 20 flights per day. At that capacity over 61 test days, both queues contain 1,220 reviews. Baseline finds 120 severe delays with 1,100 false alerts and 3,598 misses. Forest finds 239, with 981 false alerts and 3,479 misses. Severe means departure at least 60 minutes late; there are 3,718 eligible severe outcomes.

Show model choice and a small capacity control after generating measured capacity results. A simple visualization divides reviewed flights into severe delays found and other reviews; show misses alongside it. Distinguish the denominator of reviews from the denominator of all severe delays. A rounded per-100 illustration is optional and must link exact counts.

The baseline's tied scores produce a deterministic, arbitrary schedule-key queue; it is not a real airline policy or random comparator. Outcomes missing from evaluation are a visible limitation. These controls explore retrospective results and do not show intervention savings.

### 5. How trustworthy are the uncertainty ranges?

Define interval coverage in ordinary language: how often the measured delay fell inside the proposed range. For the selected median baseline, show 90% target, 85.45% measured test coverage, 90.35% November and 80.55% December, with a 56-minute interval width.

Show a target line and month comparison. The takeaway is that uncertainty must be checked over time. Do not assign this interval to the forest unless it is separately calibrated/evaluated. A constant radius does not improve rankings; a nominal coverage level is not a flight-level probability of reliability. Do not infer a causal explanation for the December change.

Expandable research note: the 2026 Japanese study forecasts daily/weekly average delays at eight airports using network features and adaptive conformal methods. The current prototype implements a simpler split-conformal flight-level experiment. Publisher snippets/institutional citation were checked; the paper's proprietary OAG data and full methods were not reproduced. Keep that distinction clear and avoid imported accuracy claims.

### 6. What should happen next?

Visible conclusion: use the diagnostics to investigate high burden; the schedule-only forecast evidence does not justify operational adoption.

Three short next steps: verify repeated patterns and source discrepancies; obtain current schedule snapshots, rotation/turnaround records and timestamped weather forecasts; agree review capacity and error costs before a prospective evaluation. Describe what the prototype currently delivers and what would be needed to test a real intervention.

Provide an **Export findings brief** action reflecting selected metric/model/capacity, the fixed study periods, sources, caveats and recommendation. Use downloadable Markdown or a print-friendly HTML layout first; do not add a document-rendering service solely for this.

### 7. Methods, research and reproducibility

Concise accordions for data sources/rights, metric definitions, validation/leakage, model/uncertainty methods, research references and future study protocol. Link code, machine-readable evidence, CI, methodology and contribution record. Show implemented/experimental/planned status without claiming all planned work is done.

Cite primary sources, including BTS, nycflights13 CC0 metadata, the Japanese paper/institutional list, and the conformal reference already recorded in docs/research.md. NABLA context belongs in a small role-relevance note: this is an independent project that could support a discovery/feasibility discussion, not a verified internal product need.

## Real implementation work required

The existing public JSON is sufficient for a first narrative page but not every planned interaction:

1. Export complete eligible monthly segment aggregates, not just each top-ten ranking. Include observed traffic, matched rate denominator, delayed count, available delay minutes and missing/flag metadata. Do not reconstruct full population statistics from a union of top-ten lists.
2. Extend the flight experiment to export capacity metrics for a finite grid such as 10, 20, 40 and 80 reviews/day, using frozen predictions, identical eligibility and deterministic ties. Preserve the original capacity-20 results. Reconcile hits + false alerts = reviews and hits + misses = severe outcomes for every grid point. Do not interpolate counts or imply rerunning a model in the browser.
3. Generate a public evidence bundle from validated reports: study identifiers, periods, grain, definitions, sources, claims and measured results. Static charts read this bundle rather than hardcoded duplicated numbers. Include a public manifest with evidence hashes and generating code revision.
4. Add tests for the exporter and capacity accounting. Preserve the existing 21 tests and frozen results. Keep source data excluded; publish only reviewed derived aggregates and rights-cleared assets.
5. Build the story surface and verify its interactions and explanations before deployment.

Future research should be documented separately: recent bounded BTS data, historical severe-rate baseline, an alert-focused validation criterion declared in advance, multiple chronological test windows and improved treatment of missing outcomes. Freeze the current experiment as the v1 evidence. Avoid fitting new models merely to make the public page's numbers look more impressive.

## Stack and file structure

Use the existing Python/DuckDB/scikit-learn analytical stack. For the public presentation, start with static HTML/CSS/JavaScript as demonstrated by the feedback project. A small maintained chart library is optional only if it materially improves accessible plotting; inspect official docs/licenses and lock any dependencies. Native forms, accessible text and small real charts are sufficient. Do not add React, a server, Streamlit, AWS CDK or an LLM chatbot merely to present saved research.

Suggested additions:

```text
site/index.html
site/styles.css
site/app.js
site/evidence.json
site/evidence.csv
site/brief.html
scripts/export_public.py
tests/test_public_export.py
docs/CLAIMS.md
docs/UI_VALIDATION.md
.github/workflows/pages.yml
```

Use relative assets and anchors that work under `/aviation-decision-support/`. Support validated URL parameters for rank, model and capacity, browser back/forward and reset. Unknown parameters fall back to documented defaults. The site should load introductory copy without JavaScript and give an intelligible evidence-loading error if its bundle fails.

## Done means verified and published

Follow docs/PUBLICATION_PLAN.md. Required evidence: local analytical checks; real generated public evidence; chart-to-report reconciliation; keyboard controls; desktop/mobile rendering; no console errors or broken source links; passing CI; successful Pages deployment; HTTP response and rendered final public URL; reload a shared interaction URL and verify the same selection.

Record a short owner-learning exercise per milestone and keep unreviewed AI-generated decisions marked pending. The page's analytical evidence should be agent-checked, but personal understanding is not implied by that check.

Final reply to the owner: working public hyperlink, concise changes, checks passed, material limitations and a short CV link label. Never present the intended URL as already live before verifying it.

## Ready-to-use execution prompt

Read `C:\Users\sayed\Documents\aviation-decision-support\SOL.md` and the linked visual/publication contracts. Implement the complete v1 interactive research story, generate and verify its evidence assets, preserve the existing pipeline and honest authorship record, publish it through GitHub Pages, inspect the public page at mobile and desktop sizes, and return its verified live hyperlink. Continue through publication within the user's authorized scope; update the handoff/status when genuine external blockers arise. Keep updates short and do not add speculative product or analytical claims.
