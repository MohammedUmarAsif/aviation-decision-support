# Interactive research page validation

Agent-checked 12 October 2026. These checks establish execution and presentation evidence, not independent peer review or personal comprehension. Local validation and public deployment verification are complete.

## Evidence

The unchanged monthly and forecast JSON results reproduced from local raw input within 1e-8 tolerance. Complete derived monthly export: 1,806 carrier-airport segments, including 931 passing the 100-flight screen. Nine missing airport-name labels retain their code fallback. Full population totals and all three top-ten rankings reconcile to `reports/audit.json`.

Measured capacity grids use the same frozen model predictions and known-outcome eligibility for 10, 20, 40 and 80 daily reviews. Capacity-20 results exactly match the frozen report. For every grid point, hits + false alerts = reviews and hits + misses = 3,718 eligible severe outcomes. No interpolation or new model tuning was performed.

Public evidence checksum (canonical LF text SHA256): `d9d7b60ea0dfb36152fb6229e3b2ab60a0c86dd59f1e7b9234762a27241f774a`. `site/manifest.json` records generating code and report hashes. Its explicit text normalization makes validation portable between Windows and Linux; original raw-source byte hashes remain unchanged in the analytical reports.

Local checks: uv locked sync, Ruff lint/format, ty and 27 pytest cases passed. Original 21 cases remain; six additional cases check complete export, unknown values, capacity clipping/accounting, frozen result reconciliation and manifest integrity. GitHub research CI also reproduces the capacity grid.

## Rendered checks

Browser: Codex in-app Chromium. Actual DOM dimensions were checked, rather than inferred from requested viewport settings. Temporary viewport overrides were reset.

| View | Observed result |
|---|---|
| Desktop 1440 × 900 | Two-column ranking with real bars, readable values and selected evidence; no page-wide overflow (document width 1425) |
| Mobile 390 × 844 | Single-column narrative, readable labels, chronological split and queue denominators; no page-wide overflow (document width 375) |
| Small mobile 320 × 844 | Heading and CTA fit; validated defaults for invalid parameters; no page-wide overflow (document width 305) |

Saved evidence: [desktop findings](screenshots/desktop-findings.jpg), [mobile opening](screenshots/mobile-opening.jpg), [mobile findings](screenshots/mobile-findings.jpg), [mobile queue](screenshots/mobile-queue.jpg). Tables scroll within their containers. Navigation controls and disclosures have comfortable touch space. No decorative raster assets or third-party runtime/font dependencies are used.

Observed interactions: three rankings; Delta–Atlanta/AA–DFW selection and QX–SFO rate denominator; complete eligible segment selector; both models at every capacity; eight keyboard-operated disclosures; select arrow keys and Tab to visible outlined chart focus; share URL reload; back/forward; invalid parameters; reset; Markdown brief download. The downloaded AA–DFW/forest/80 brief included 4,880 reviews, 818 severe delays found, 4,062 false alerts and 2,900 misses, plus study dates, sources and limitations.

A separate local fixture without the evidence asset showed a clear HTTP 404 evidence-loading message and kept controls disabled. Introductory explanation is static HTML and remains available without JavaScript. The main-page console showed no warnings or errors. Rendered inspection caught and fixed missing source-name handling and an inline chart-track display issue before publication.

Measured WCAG contrast ratios: primary ink/paper 14.26; muted text/paper 6.56; white/primary button 7.03; blue/blue-soft 6.21; limitation text/amber-soft 6.76; muted text/blue-soft 5.97; focus ring/paper 5.19. Text colors clear the 4.5:1 AA threshold; the focus ring clears 3:1.

## Limits

No current operational validity, aviation-safety suitability, causal benefit, cancellation performance or affiliation claim. Baseline ties remain arbitrary; the forest lost validation MAE; median intervals undercovered; raw BTS acquisition history is partly verified. Owner-learning answers beyond the two previously recorded elementary exercises remain pending.

## Verified public release

Live root: https://mohammedumarasif.github.io/aviation-decision-support/. Implementation revision `0a4c07396dce700d10d775628154782259ab629a` passed [quality/research CI](https://github.com/MohammedUmarAsif/aviation-decision-support/actions/runs/38184737187) and [Pages validation, build and deployment](https://github.com/MohammedUmarAsif/aviation-decision-support/actions/runs/38184737399). Docker and full pinned NYC forecast/capacity reproduction passed on Linux. Pages uploads only `site/`, after those checks succeed; it does not run live Python inference.

Public root, stylesheet, JavaScript, evidence JSON, aggregate CSV and manifest returned HTTP 200. Public JSON/CSV canonical hashes matched the deployed manifest. Public rendered dimensions were again measured at 1440 × 900 and 390 × 844, with no page-wide overflow and no console warning/error logs. [Public desktop](screenshots/public-desktop.jpg) and [public mobile](screenshots/public-mobile.jpg) show the deployed result.

Reloading [a shared rate/baseline/40 state](https://mohammedumarasif.github.io/aviation-decision-support/?rank=delay_rate&model=train_median&capacity=40&segment=QX-SFO#ranking-title) preserved QX–SFO, 113/149 = 75.84%, and the baseline queue: 2,440 reviews, 246 severe delays found, 2,194 false alerts and 3,472 misses. The downloaded public brief matched these counts, sources and limits; reset restored the default forest/20 state. Temporary viewport overrides were reset after validation.

External links to BTS, pinned nycflights13 and its CC0 metadata, DOI, arXiv, GitHub reports/docs and CI returned HTTP 200. The institutional journal list rendered successfully in the actual browser and corroborated the 2026 citation; Python's direct request had a host-specific certificate-chain issue. No certificate warning was bypassed, and no unavailable full-text research reproduction is claimed.

CV label: **Aviation Decision Support — Interactive Research Study**, linked to the live root.
