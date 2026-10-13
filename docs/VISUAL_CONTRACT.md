# Aviation research page visual contract

Design proposal dated 12 October 2026. This is an implementation contract, not evidence that the website has been built or visually validated.

Owner approval, 13 October 2026: publish the compact research journey reviewed in the local preview. Retain navy/blue with sunset-orange chapter accents, the supplied StockCake image with a small subdued corner credit, clearly explained contributions and a retrospective demo at the end. The full prior explorer remains available from the narrative. This supersedes earlier landing order and navigation directions. Preserve frozen evidence and source/limitation access.

Owner amendment, 12 October 2026: replace the bright light surface with a consistent
airport-at-night navy theme, muted blue evidence accents and warm amber caveats.
Use clearly labelled illustrative aviation imagery, retain the measured charts and
provide source-backed context connecting reliability, workload, review capacity and
forecast assurance. The earlier light-surface direction below is superseded.

## Audience and direction

Reading this as an interactive research case study for recruiters and researchers, with a calm, readable design and a guided journey from problem to recommendation. This is a new public presentation surface for the existing analytical project.

Use the user-level design-taste-frontend skill for the landing/story surface. Its dashboard and dense-table exclusions apply: this page should contain focused evidence charts and small accessible tables, not an admin dashboard. The user requested a simple contextual explanation and useful interaction. Those requirements take priority over decorative defaults.

DESIGN_VARIANCE: 4. MOTION_INTENSITY: 2. VISUAL_DENSITY: 3.

## Reference review

Reviewed in the browser on 12 October 2026:

- https://mohammedumarasif.github.io/customer-feedback-intelligence/#main
- https://mohammedumarasif.github.io/fenland-carbon-lab/?public-family=weather-&public-target=nee&public-split=test&public-seed=17#main

Customer Feedback Intelligence: light background, teal emphasis, strong sans-serif question, compact chapter navigation, plain-language findings, chronological evaluation strip, human-review illustration, example interaction and expandable methods. The category suggestion interaction was exercised. Its mobile review section was inspected at 390px width.

Fenland Carbon Lab: dark green editorial surface, prominent question, honest model-comparison finding, evidence filters, linked aggregate results, methods and reproduction artifacts. Desktop rendering was inspected. A browser-scoped mobile resize did not apply to its background tab, so a mobile visual claim is not made here. The implementation agent must validate the new aviation page at both target sizes.

Borrow the feedback site's accessible narrative and the carbon site's traceable evidence. Improve novice entry by defining the dataset and units before presenting advanced metrics. Keep the reference sites unchanged; do not copy whole sections or adopt their scientific claims.

## Visual system

- Working name: Flight Review. Subtitle: Aviation data and forecast evaluation.
- Light reading surface, deep ink text, restrained blue emphasis, warm amber for limitations. Color choices must pass measured contrast checks; these directions are not validated color tokens.
- One sans-serif family with a system fallback. Use a self-hosted font only if it improves clarity; avoid adding font/network dependencies merely for branding.
- Content width about 1120px; prose width about 65 characters. Body 16–18px with comfortable line spacing. Heading scale should fit a 390px viewport without clipping.
- Stable, compact navigation: Findings, Forecasts, Methods, Next steps; GitHub as a secondary link. Skip link and clear keyboard focus.
- One main question and one primary action in the opening. Show a real evidence visualization below it rather than a decorative aircraft image or fake product screenshot.
- Low-motion state changes. No autoplay, carousel, scroll hijacking or mandatory animation.
- Deliberate section rhythm: question/prose, ranking chart, data strip, time split, comparison, coverage chart, recommendation. Avoid repeating equal card grids throughout.
- Each visible section should answer one question. Aim for 40–70 words of visible explanation; put detailed methods, glossary, references and tables in clearly named disclosure panels.
- Each chart has a title, units, denominator, date/geography label, a brief takeaway and a table alternative. Color is supplemented with labels/shapes.
- Use names such as Delta and Atlanta; retain DL–ATL as secondary text. Distinguish arrival airport from origin airport in the two studies.
- Important limits remain visible near the associated result. Do not bury geographic/temporal restrictions or failed uncertainty coverage in the footer.

## Responsive behavior

Required implementation checks: desktop 1440×900 and mobile 390×844, plus a 320px overflow check. Browser viewport overrides are temporary and must be reset after validation.

At mobile widths: single-column story, large touch targets, labels above controls, charts with readable values, no page-wide horizontal scrolling. A researcher table may scroll within its labeled container. Navigation must remain usable without covering anchor headings. Disclosure controls must be operable by keyboard and touch.

## Interaction rules

- Useful interactions explain a decision, compare evidence, or reveal reproducibility details.
- Initial state is fully populated and tells the default story without requiring a filter choice.
- Avoid more than one primary control group visible per section.
- Clearly label retrospective exploration. Clicking a control does not train a model or change the frozen experiment.
- No arbitrary uploads or live prediction form in the first release. All public data must be approved export artifacts with known provenance.
- Share the selected ranking, model and capacity through URL parameters, with validation/defaults and a reset action. Do not copy the carbon site's irrelevant seed/target parameters.
- Download a brief reflecting the selected state; its main conclusion and caveats must agree with the visible chart.

## Publication presentation

Use a descriptive page title, meta description, canonical project URL and accessible social preview. Social preview values must be generated from the same evidence as the page. Provide plain source/reproduction links and AI-assistance disclosure. Do not use NABLA logos, affiliation language, invented testimonials or production claims.

Success means a visitor can explain the problem, data, measured result and recommendation in three minutes, then follow a source link to reproduce or inspect the methods.
